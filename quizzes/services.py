import json
import os
import urllib.request


def fallback_questions(subject_name, chapter):
    return [
        {
            "question": f"What is an important idea from {chapter} in {subject_name}?",
            "option_a": "A key fact from the lesson",
            "option_b": "An unrelated topic",
            "option_c": "A random guess",
            "option_d": "None of these",
            "correct_option": "A",
            "explanation": "Review the chapter notes and match the question with the main concept.",
        },
        {
            "question": f"How should a learner prepare for {chapter}?",
            "option_a": "Skip class",
            "option_b": "Read, practice, and ask questions",
            "option_c": "Ignore homework",
            "option_d": "Only memorize answers",
            "correct_option": "B",
            "explanation": "Practice and questions build stronger understanding.",
        },
    ]


def generate_questions(subject_name, chapter, count=5):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return fallback_questions(subject_name, chapter)

    prompt = (
        f"Create {count} primary-school multiple choice quiz questions for {subject_name}, chapter {chapter}. "
        "Return only JSON list objects with question, option_a, option_b, option_c, option_d, correct_option, explanation."
    )
    data = json.dumps(
        {
            "model": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.4,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=data,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
        content = payload["choices"][0]["message"]["content"]
        return json.loads(content)
    except Exception:
        return fallback_questions(subject_name, chapter)
