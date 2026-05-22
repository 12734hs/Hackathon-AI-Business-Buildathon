import os
import requests
import json


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def fallback_analysis(current_profile, peer_profile, common_points, complementary_points):
    their_goal = peer_profile.get("careerGoal", "their field")

    why = f"You share common interests in {', '.join(common_points[:3]) if common_points else 'technology and innovation'}."

    how = (
        f"You can help each other by combining your skills. "
        f"They are focused on {their_goal}, which complements your background."
    )

    what = [
        "Build a project together at a hackathon",
        "Share knowledge and resources with each other",
        "Collaborate on an open-source or side project"
    ]

    return {
        "whyMatch": why,
        "howYouCanHelpEachOther": how,
        "whatYouCanDoTogether": what
    }


def generate_ai_analysis(current_profile, peer_profile, common_points, complementary_points):
    groq_api_key = os.getenv("GROQ_API_KEY", "")

    print("[ai.py] GROQ_API_KEY exists:", bool(groq_api_key))

    if not groq_api_key:
        return fallback_analysis(current_profile, peer_profile, common_points, complementary_points)

    prompt = f"""
You are a hackathon team matchmaker. Given two people's profiles, write a short match analysis.

Person A:
- Career Goal: {current_profile.get("careerGoal", "")}
- Skills: {", ".join(current_profile.get("skills", []))}
- Interests: {", ".join(current_profile.get("interests", []))}
- Hobbies: {", ".join(current_profile.get("hobbies", []))}
- Education: {current_profile.get("education", "")}

Person B:
- Career Goal: {peer_profile.get("careerGoal", "")}
- Skills: {", ".join(peer_profile.get("skills", []))}
- Interests: {", ".join(peer_profile.get("interests", []))}
- Hobbies: {", ".join(peer_profile.get("hobbies", []))}
- Education: {peer_profile.get("education", "")}

Things they have in common: {", ".join(common_points) if common_points else "None listed"}
Complementary strengths: {", ".join(complementary_points) if complementary_points else "None listed"}

Respond ONLY with a valid JSON object in this exact format:
{{
  "whyMatch": "One or two sentences explaining why they are a good match.",
  "howYouCanHelpEachOther": "One or two sentences on how they can help each other.",
  "whatYouCanDoTogether": [
    "First concrete project or activity idea",
    "Second concrete project or activity idea",
    "Third concrete project or activity idea"
  ]
}}

Do not include markdown.
Do not include any text outside the JSON object.
"""

    try:
        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }

        body = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant that returns only valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.4,
            "max_tokens": 500
        }

        response = requests.post(GROQ_API_URL, headers=headers, json=body, timeout=15)
        response.raise_for_status()

        data = response.json()
        raw_text = data["choices"][0]["message"]["content"].strip()

        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]
            raw_text = raw_text.strip()

        result = json.loads(raw_text)

        if (
            "whyMatch" not in result
            or "howYouCanHelpEachOther" not in result
            or "whatYouCanDoTogether" not in result
        ):
            raise ValueError("Missing required keys in AI response")

        return result

    except Exception as e:
        print(f"[ai.py] Groq AI failed: {e}. Using fallback.")
        return fallback_analysis(current_profile, peer_profile, common_points, complementary_points)