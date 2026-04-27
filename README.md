# Smart Hospital Queue & Emergency Bed Allocation System

A **Django-based smart hospital mini project** that helps hospitals **prioritize patients intelligently**, **manage emergency queues**, and **allocate beds based on patient severity**.

This project was built as a **PBL (Project-Based Learning) college project** to simulate a real-world hospital workflow where **critical patients are treated first** and **beds are allocated efficiently**.

---

## Live Project Idea

This system improves hospital workflow by:

* Registering patients with symptoms and emergency status
* Analyzing patient condition using **Google Gemini AI**
* Falling back to **rule-based triage** if AI is unavailable
* Generating a **priority score**, **severity level**, and **recommended department**
* Automatically creating a **smart queue**
* Assigning the **best available bed** based on severity
* Tracking completed patients in **history**

---

## Features

*  Patient registration with:

  * Name
  * Age
  * Gender
  * Multiple symptom selection
  * Additional notes/problem
  * Emergency case flag

*  AI-assisted smart triage using:

  * **Google Gemini API**
  * **Fallback rule-based logic** if AI fails

*  Automatic generation of:

  * **Priority Score**
  * **Severity Level** (`Critical`, `High`, `Medium`, `Low`)
  * **Recommended Department**

*  Smart queue management:

  * Patients are sorted by **highest priority first**
  * More critical patients are handled before low-risk patients

*  Smart bed allocation:

  * **Critical** → ICU preferred
  * **High** → Emergency bed preferred
  * **Medium / Low** → General bed preferred

*  Dashboard pages for:

  * Active patient queue
  * Completed patient history
  * Bed availability tracking

*  Django Admin support for:

  * Patients
  * Beds
  * Queue entries

---

##  Problem Statement

In many hospitals, patients are often handled using a **first-come, first-served** approach. This can delay treatment for **critical or emergency cases**. Bed allocation is also often manual, which may lead to inefficient resource usage.

### This project solves that by:

* capturing symptoms during registration
* identifying emergency cases
* calculating treatment priority automatically
* sorting patients intelligently in the queue
* allocating the most suitable available bed based on severity

---

##  Solution Flow

```text id="n9lvy4"
Patient Registration
        ↓
Symptoms + Emergency Input
        ↓
AI / Fallback Triage Logic
        ↓
Priority Score + Severity + Department
        ↓
Queue Entry Created
        ↓
Smart Queue Sorting
        ↓
Severity-Based Bed Allocation
        ↓
Treatment Completion
        ↓
Bed Released + Record Added to History
```

---

## Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML, CSS
* **Database:** SQLite (default Django database)
* **AI Integration:** Google Gemini API
* **Environment Variables:** python-dotenv

---

##  Project Structure

```bash id="7i5k74"
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

> **Note:** The exact folder layout may vary slightly depending on your local setup, but these are the main project components.

---

## How It Works

### 1) Patient Registration

Hospital staff enters:

* patient name
* age
* gender
* symptoms
* additional notes
* emergency status

### 2) Smart Triage (AI + Fallback)

The system analyzes the patient using:

* **Google Gemini AI**, or
* **fallback rule-based logic** if AI is unavailable

It returns:

* **priority score**
* **severity**
* **recommended department**

### 3) Smart Queue Creation

After analysis:

* the patient is saved
* a queue token is generated
* the patient is added to the active queue

### 4) Smart Queue Sorting

Patients are automatically sorted by:

* **higher priority score first**
* then **token order**

### 5) Smart Bed Allocation

Beds are assigned based on severity:

* **Critical** → ICU → Emergency → General
* **High** → Emergency → ICU → General
* **Medium** → General → Emergency → ICU
* **Low** → General → Emergency → ICU

### 6) Completion & History

When treatment is completed:

* assigned bed becomes available again
* patient status becomes **Completed**
* record appears in **Queue History**

---

## Installation & Setup

### 1) Clone the repository

```bash id="fpc4n5"
git clone https://github.com/Arryan2005/PBL-Project.git
cd PBL-Project
```

### 2) Create a virtual environment (recommended)

```bash id="ggkk8x"
python -m venv venv
```

### 3) Activate the virtual environment

**Windows**

```bash id="nng31j"
venv\Scripts\activate
```

**Mac/Linux**

```bash id="9b7d5c"
source venv/bin/activate
```

### 4) Install dependencies

```bash id="njlwmn"
pip install -r requirements.txt
```

### 5) Create a `.env` file in the project root

```env id="mwvjlwm"
GEMINI_API_KEY=your_api_key_here
```

> If the Gemini API is unavailable, the system will still work using fallback logic.

### 6) Run migrations

```bash id="v1djlwm"
python manage.py makemigrations
python manage.py migrate
```

### 7) Create superuser (optional, for admin access)

```bash id="3etjlwm"
python manage.py createsuperuser
```

### 8) Start the development server

```bash id="1kjjlwm"
python manage.py runserver
```

### 9) Open in browser

```bash id="gmdjlwm"
http://127.0.0.1:8000/
```

---
