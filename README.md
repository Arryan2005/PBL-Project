# Smart Hospital Queue & Emergency Bed Allocation System

A Django-based college project for smart patient triage, emergency queue management, and intelligent bed allocation.

## Features
- Patient registration with multiple symptom selection
- Emergency flag support
- Weighted priority score calculation
- Severity classification (Critical / High / Medium / Low)
- Department recommendation based on symptoms
- Live queue dashboard
- Smart bed allocation based on severity and bed type
- Queue history for completed patients
- Bed dashboard for availability tracking

## Tech Stack
- Python
- Django
- HTML
- CSS

## Team Modules
- Frontend & UI
- Patient Registration & Smart Queue Logic
- Bed Management & Queue Operations
- Routing, Testing & Documentation

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt

2. Run Migrations:
    py manage.py makemigrations
    py manage.py migrate

3. Start server:
    py manage.py runserver

4. Open in browser:
    http://127.0.0.1:8000/