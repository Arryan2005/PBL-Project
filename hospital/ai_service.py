import google.generativeai as genai
import json
from django.conf import settings


def analyze_patient_with_ai(name, age, gender, problems, other_problem, is_emergency):
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
You are a medical triage AI assistant in a hospital emergency system.
Analyze the following patient information and return a structured JSON response.

Patient Details:
- Name: {name}
- Age: {age}
- Gender: {gender}
- Reported Symptoms/Problems: {', '.join(problems) if problems else 'None'}
- Additional Notes: {other_problem if other_problem else 'None'}
- Marked as Emergency by staff: {'Yes' if is_emergency else 'No'}

Provide:
1. priority_score: 0 to 100 (100 = most critical)
2. severity: exactly one of → "Critical", "High", "Medium", "Low"
3. recommended_department: e.g. Cardiology, Neurology, Emergency, General Medicine
4. ai_reasoning: 1-2 sentence clinical explanation

Respond ONLY with a valid JSON object. No markdown, no extra text.

Example:
{{
  "priority_score": 85,
  "severity": "Critical",
  "recommended_department": "Cardiology",
  "ai_reasoning": "Chest pain in elderly patient suggests possible cardiac emergency."
}}
"""

    response = model.generate_content(prompt)

    # Strip markdown code fences if Gemini adds them
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    text = text.strip()

    result = json.loads(text)

    # Safety validation
    result['priority_score'] = max(0, min(100, int(result.get('priority_score', 50))))
    if result.get('severity') not in ['Critical', 'High', 'Medium', 'Low']:
        result['severity'] = 'Medium'

    return result


def get_ai_analysis_safe(name, age, gender, problems, other_problem, is_emergency):
    """Calls Gemini AI. Falls back to basic scoring if API fails."""
    try:
        return analyze_patient_with_ai(
            name, age, gender, problems, other_problem, is_emergency
        )
    except Exception as e:
        print(f"[Gemini AI Error] {e}")
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