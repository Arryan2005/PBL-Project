# Smart Hospital Queue & Emergency Bed Allocation System

A modern **Django-based smart hospital management system** that helps hospitals intelligently prioritize patients, manage emergency queues, and allocate beds based on patient severity.
This project was developed as a **Project-Based Learning (PBL)** mini project to simulate real-world hospital workflows where **critical patients are treated first** instead of using a traditional first-come, first-served system.

---

# Project Overview

The Smart Hospital Queue & Emergency Bed Allocation System improves hospital workflow by combining:

* AI-assisted patient triage
* Smart priority-based queue management
* Intelligent bed allocation
* Emergency handling
* Real-time hospital dashboards

The system automatically analyzes patient conditions using AI and generates:

* Priority Score
* Severity Level
* Recommended Department

Patients are then placed into a dynamically sorted smart queue where critical patients receive faster attention.

---

# Key Features

## Smart Patient Registration

Hospital staff can:

* Register patients
* Enter symptoms/problems
* Add additional medical notes
* Mark emergency cases

---

## AI-Assisted Smart Triage

The system uses:

* **Groq API**
* **Llama 3.3 70B Versatile Model**

for intelligent patient analysis.

The AI generates:

* Priority score (0–100)
* Severity level
* Recommended department
* Clinical reasoning

### Severity Levels

* Critical
* High
* Medium
* Low

---

## Fallback Rule-Based System

If the AI API becomes unavailable, the application automatically switches to a fallback rule-based logic system.

This ensures the hospital workflow continues without interruption.

---

## Smart Queue Management

Patients are automatically sorted using:

1. Highest priority score first
2. Token order second

This ensures emergency and critical patients receive treatment before low-risk cases.

---

## Smart Bed Allocation

Beds are assigned automatically according to patient severity.

### Bed Allocation Logic

| Severity | Preferred Bed Allocation  |
| -------- | ------------------------- |
| Critical | ICU → Emergency → General |
| High     | Emergency → ICU → General |
| Medium   | General → Emergency → ICU |
| Low      | General → Emergency → ICU |

---

## Dashboard System
The project includes multiple dashboards:

* Patient Registration Dashboard
* Active Queue Dashboard
* Completed Patient History
* Bed Management Dashboard

---

## Django Admin Support
Admin panel support for:

* Patients
* Beds
* Queue Entries

---

#  Problem Statement

In many hospitals, patient treatment follows a **first-come, first-served** workflow.
This may delay treatment for:

* emergency patients
* critical cases
* elderly patients
* accident victims

Bed allocation is also often manual and inefficient.

---

# Proposed Solution

This project solves the problem by:

* analyzing symptoms intelligently
* identifying emergency cases
* generating automatic treatment priority
* creating a smart hospital queue
* allocating beds based on severity
* improving resource utilization

---

# ⚙️ System Workflow

```text
Patient Registration
        ↓
Symptoms + Emergency Input
        ↓
AI / Fallback Triage Analysis
        ↓
Priority Score + Severity + Department
        ↓
Queue Entry Creation
        ↓
Smart Queue Sorting
        ↓
Severity-Based Bed Allocation
        ↓
Treatment Completion
        ↓
Bed Released + History Updated
```

---

# Tech Stack

| Category              | Technologies             |
| --------------------- | ------------------------ |
| Backend               | Python, Django           |
| Frontend              | HTML, CSS                |
| Database              | SQLite                   |
| AI Integration        | Groq API + Llama 3.3 70B |
| Environment Variables | python-dotenv            |

---

# Project Structure

```bash
PBL-Project/
│
├── manage.py
├── requirements.txt
├── README.md
│
├── hospital/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── ai_service.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── add_patient.html
│   │   ├── queue_list.html
│   │   ├── queue_history.html
│   │   └── bed_dashboard.html
│   │
│   └── static/
│       └── css/
│           └── style.css
│
└── smart_hospital/
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    └── asgi.py
```

---

#  Database Models

## Patient

Stores:

* Name
* Age
* Gender
* Symptoms
* Emergency status
* Priority score
* Severity
* Recommended department

---

## Bed

Stores:

* Bed number
* Bed type
* Availability status

Bed types:

* ICU
* Emergency
* General

---

## QueueEntry

Stores:

* Queue token
* Patient reference
* Assigned bed
* Queue status

Statuses:

* Waiting
* Assigned
* Completed

---

#  Smart Logic Used

## Queue Prioritization

Patients are sorted using:

```python
order_by('-patient__priority_score', 'token_number')
```

Higher priority patients are treated first.

---

## Severity-Based Bed Matching

The system automatically selects the best available bed depending on severity.

Example:

* Critical patients get ICU preference
* High-risk patients get emergency beds
* Normal patients get general beds

---

## AI Prompt Engineering

The AI model analyzes:

* symptoms
* age
* emergency status
* additional notes

and returns structured JSON containing:

* priority score
* severity
* department recommendation
* reasoning

---

# 🎨 Frontend Features

The UI includes:

* Responsive dashboard design
* Modern hospital-themed interface
* Severity badges
* Smart queue tables
* Real-time bed status display
* Glassmorphism-inspired styling

---

# 📸 Main Pages

## ➕ Add Patient

Register and analyze patients.

## 📋 Active Queue

Monitor active patients and assign beds.

## 🛏️ Bed Dashboard

Track bed availability and occupancy.

## 📜 Queue History

View completed patient records.

---

# 🛠️ Installation & Setup

## 1) Clone Repository

```bash
git clone https://github.com/Arryan2005/PBL-Project.git
cd PBL-Project
```

---

## 2) Create Virtual Environment

```bash
python -m venv venv
```

---

## 3) Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## 4) Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5) Create `.env` File

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_api_key_here
```

---

## 6) Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 7) Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

---

## 8) Run Development Server

```bash
python manage.py runserver
```

---

## 9) Open in Browser

```text
http://127.0.0.1:8000/
```