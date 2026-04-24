from django.shortcuts import render, redirect, get_object_or_404
from .forms import PatientForm
from .models import Patient, QueueEntry, Bed
from .ai_service import get_ai_analysis_safe


# -----------------------------
# SMART LOGIC FUNCTIONS (kept as fallback inside ai_service.py)
# -----------------------------

def get_best_bed_for_severity(severity):
    """
    Smart bed allocation logic based on severity.
    """
    if severity == "Critical":
        return (
            Bed.objects.filter(is_available=True, bed_type='ICU').first()
            or Bed.objects.filter(is_available=True, bed_type='Emergency').first()
            or Bed.objects.filter(is_available=True, bed_type='General').first()
        )

    elif severity == "High":
        return (
            Bed.objects.filter(is_available=True, bed_type='Emergency').first()
            or Bed.objects.filter(is_available=True, bed_type='ICU').first()
            or Bed.objects.filter(is_available=True, bed_type='General').first()
        )

    elif severity == "Medium":
        return (
            Bed.objects.filter(is_available=True, bed_type='General').first()
            or Bed.objects.filter(is_available=True, bed_type='Emergency').first()
            or Bed.objects.filter(is_available=True, bed_type='ICU').first()
        )

    else:  # Low
        return (
            Bed.objects.filter(is_available=True, bed_type='General').first()
            or Bed.objects.filter(is_available=True, bed_type='Emergency').first()
            or Bed.objects.filter(is_available=True, bed_type='ICU').first()
        )


# -----------------------------
# MAIN VIEWS
# -----------------------------

def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            selected_problems = form.cleaned_data['problems']
            other_problem = form.cleaned_data['other_problem']

            # Combine selected symptoms + other problem into one text field
            all_problems = ", ".join(selected_problems)

            if other_problem:
                if all_problems:
                    all_problems += ", " + other_problem
                else:
                    all_problems = other_problem

            patient = form.save(commit=False)
            patient.problem = all_problems
            patient.other_problem = other_problem

            # 🤖 Gemini AI logic
            ai_result = get_ai_analysis_safe(
                name=patient.name,
                age=patient.age,
                gender=patient.gender,
                problems=list(selected_problems),
                other_problem=other_problem,
                is_emergency=patient.is_emergency
            )
            patient.priority_score = ai_result['priority_score']
            patient.severity       = ai_result['severity']
            patient.recommended_department = ai_result['recommended_department']

            patient.save()

            token = QueueEntry.objects.count() + 1
            QueueEntry.objects.create(
                patient=patient,
                token_number=token,
                status="Waiting"
            )

            return redirect('queue_list')
    else:
        form = PatientForm()

    return render(request, 'add_patient.html', {'form': form})


def queue_list(request):
    queue = QueueEntry.objects.exclude(status="Completed").order_by(
        '-patient__priority_score',
        'token_number'
    )

    return render(request, 'queue_list.html', {'queue': queue})


def queue_history(request):
    history = QueueEntry.objects.filter(status="Completed").order_by('-id')
    return render(request, 'queue_history.html', {'history': history})


def bed_dashboard(request):
    beds = Bed.objects.all().order_by('bed_number')
    total_beds = beds.count()
    available_beds = beds.filter(is_available=True).count()
    occupied_beds = beds.filter(is_available=False).count()

    context = {
        'beds': beds,
        'total_beds': total_beds,
        'available_beds': available_beds,
        'occupied_beds': occupied_beds,
    }

    return render(request, 'bed_dashboard.html', context)


def assign_bed(request, queue_id):
    entry = get_object_or_404(QueueEntry, id=queue_id)

    if not entry.assigned_bed and entry.status != "Completed":
        best_bed = get_best_bed_for_severity(entry.patient.severity)

        if best_bed:
            entry.assigned_bed = best_bed
            entry.status = "Assigned"
            entry.save()

            best_bed.is_available = False
            best_bed.save()

    return redirect('queue_list')


def complete_patient(request, queue_id):
    entry = get_object_or_404(QueueEntry, id=queue_id)

    if entry.assigned_bed:
        bed = entry.assigned_bed
        bed.is_available = True
        bed.save()
        entry.assigned_bed = None

    entry.status = "Completed"
    entry.save()

    return redirect('queue_list')