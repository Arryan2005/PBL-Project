from django.db import models


class Patient(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    # Combined symptoms/problems stored as text
    problem = models.TextField()

    # Extra details entered manually
    other_problem = models.CharField(max_length=200, blank=True, null=True)

    is_emergency = models.BooleanField(default=False)

    # Smart logic fields
    priority_score = models.IntegerField(default=0)
    severity = models.CharField(max_length=20, default='Low')
    recommended_department = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Bed(models.Model):
    BED_TYPES = [
        ('General', 'General'),
        ('Emergency', 'Emergency'),
        ('ICU', 'ICU'),
    ]

    bed_number = models.CharField(max_length=20, unique=True)
    bed_type = models.CharField(max_length=20, choices=BED_TYPES)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.bed_number} ({self.bed_type})"


class QueueEntry(models.Model):
    STATUS_CHOICES = [
        ('Waiting', 'Waiting'),
        ('Assigned', 'Assigned'),
        ('Completed', 'Completed'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    token_number = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Waiting')
    assigned_bed = models.ForeignKey(Bed, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token {self.token_number} - {self.patient.name}"