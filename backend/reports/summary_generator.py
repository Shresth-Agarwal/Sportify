import google.generativeai as genai
import json
from dotenv import load_dotenv
import os
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


import json

def generate_summary_with_gemini(athlete_data: dict) -> dict:
    """
    Generates a performance summary for an athlete using the Gemini model.
    """
    prompt = f"""
    You are an expert sports coach generating athlete performance summaries.

    Athlete Data (JSON):
    {json.dumps(athlete_data, indent=2)}

    Task:
    - Generate a **summary** of the athlete's performance.
    - Include a benchmark (Below Average / Average / Above Average / Elite).
    - Provide short coach feedback (2–3 sentences).
    - Return ONLY valid JSON in this format:

    {{
      "information": "...",
      "Summary": "...",
      "Coach Feedback": "..."
    }}
    """
    
    # Replace `model` with your actual Gemini model instance
    response = model.generate_content(prompt)

    raw_response_text = response.text.strip()
    summary = {}

    try:
        summary = json.loads(raw_response_text)
    except json.JSONDecodeError:
        if raw_response_text.startswith("```json") and raw_response_text.endswith("```"):
            clean_json_str = raw_response_text.replace("```json", "").replace("```", "").strip()
            try:
                summary = json.loads(clean_json_str)
            except json.JSONDecodeError:
                print(f"Error: Unable to parse cleaned JSON string. Received: {clean_json_str}")
                summary = {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print(f"Problematic response text was: {raw_response_text}")
        summary = {}

    # Corrected return statement with matching keys
    if not summary:
        return {
            "information": "Unable to generate information.",
            "Summary": "Unable to generate summary. Please try again.",
            "Coach Feedback": "Unable to provide feedback."
        }
    else:
        return summary


if __name__ == "__main__":
    athlete_data = {
    "exercise_type": "Pushup",
    "total_repetitions": 76,
    "workout_duration_sec": 76.65,
    "average_rep_time": 0.78,
    "min_angle_range": [
        56.05,
        149.47
    ],
    "workout_intensity": "High",
    "form_feedback": [
        "Form Issue: Go lower for a full range of motion.",
        "Form Issue: Keep your body straight to avoid sagging your hips.",
        "Form Issue: Keep your neck aligned with your spine."
    ]
    }
        
    

    summary = generate_summary_with_gemini(athlete_data)
    print(summary)
