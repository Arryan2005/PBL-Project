import json
import re
from groq import Groq
from django.conf import settings


def analyze_patient_with_ai(name, age, gender, problems, other_problem, is_emergency):
    client = Groq(api_key=settings.GROQ_API_KEY)

    prompt = f"""
You are a medical triage AI in a hospital emergency system.
Analyze the patient below and return a JSON object. Nothing else. No markdown.

Patient:
- Name: {name}
- Age: {age}
- Gender: {gender}
- Symptoms: {', '.join(problems) if problems else 'None'}
- Extra Notes: {other_problem or 'None'}
- Staff-marked Emergency: {'Yes' if is_emergency else 'No'}

Scoring rules:
- priority_score: integer 0–100. Higher = more urgent.
  Weight heavily: chest pain, breathlessness, stroke signs, trauma, loss of consciousness.
  Boost by 20 if staff-marked emergency. Boost by 10 if age < 5 or age > 70.
- severity: "Critical" (80–100) | "High" (60–79) | "Medium" (40–59) | "Low" (0–39)
- recommended_department: single department name e.g. Cardiology, Neurology, Emergency, Orthopedics
- ai_reasoning: max 20 words. Clinical reason only.

Return exactly:
{{
  "priority_score": <int>,
  "severity": "<Critical|High|Medium|Low>",
  "recommended_department": "<string>",
  "ai_reasoning": "<string>"
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    text = response.choices[0].message.content.strip()
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in response")
    result = json.loads(match.group())
    result['priority_score'] = max(0, min(100, int(result.get('priority_score', 50))))
    if result.get('severity') not in ['Critical', 'High', 'Medium', 'Low']:
        result['severity'] = 'Medium'

    return result


def get_ai_analysis_safe(name, age, gender, problems, other_problem, is_emergency):
    try:
        return analyze_patient_with_ai(
            name, age, gender, problems, other_problem, is_emergency
        )
    except Exception as e:
        print(f"[Groq AI Error] {e}")
        score = 50
        if is_emergency:
            score += 30
        if age:
            try:
                a = int(str(age))
                if a > 70 or a < 5:
                    score += 10
            except:
                pass
        return {
            "priority_score": min(score, 100),
            "severity": "High" if score >= 70 else "Medium",
            "recommended_department": "General Medicine",
            "ai_reasoning": "AI unavailable — basic rules applied."
        }