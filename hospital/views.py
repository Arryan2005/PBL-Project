from django.shortcuts import render, redirect, get_object_or_404
from .forms import PatientForm
from .models import Patient, QueueEntry, Bed


# -----------------------------
# SMART LOGIC FUNCTIONS
# -----------------------------

def calculate_priority(patient, selected_problems):
    score = 0

    # Emergency gets strong boost
    if patient.is_emergency:
        score += 50

    # Age-based risk
    if patient.age > 60:
        score += 10
    elif patient.age < 5:
        score += 10

    # Symptom-based weighted scoring
    symptom_scores = {
        'Chest Pain': 20,
        'Breathing Problem': 25,
        'Fever': 5,
        'Headache': 5,
        'Accident': 30,
        'Bleeding': 20,
        'Unconscious': 40,
        'Weakness': 8,
    }

    for symptom in selected_problems:
        score += symptom_scores.get(symptom, 0)

    # Bonus for multiple severe symptoms
    severe_symptoms = {'Chest Pain', 'Breathing Problem', 'Accident', 'Bleeding', 'Unconscious'}
    severe_count = len([s for s in selected_problems if s in severe_symptoms])

    if severe_count >= 2:
        score += 15

    # Bonus if user typed extra problem text
    if patient.other_problem:
        score += 5

    return score


def get_severity(score):
    if score >= 90:
        return "Critical"
    elif score >= 65:
        return "High"
    elif score >= 35:
        return "Medium"
    else:
        return "Low"


def get_recommended_department(selected_problems):
    if 'Accident' in selected_problems or 'Bleeding' in selected_problems:
        return "Trauma / Emergency"
    elif 'Unconscious' in selected_problems:
        return "Emergency / ICU"
    elif 'Chest Pain' in selected_problems:
        return "Cardiology"
    elif 'Breathing Problem' in selected_problems:
        return "Pulmonology / Emergency"
    elif 'Fever' in selected_problems or 'Weakness' in selected_problems:
        return "General Medicine"
    elif 'Headache' in selected_problems:
        return "Neurology / General Medicine"
    else:
        return "General Medicine"


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

            # Smart logic
            patient.priority_score = calculate_priority(patient, selected_problems)
            patient.severity = get_severity(patient.priority_score)
            patient.recommended_department = get_recommended_department(selected_problems)

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