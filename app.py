"""
AI-Powered Email Assistant
Backend: Flask + Groq API (Free, Ultra-fast Llama 3.3 70B)
"""

import os
import json
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Email tone templates
TONE_PROMPTS = {
    "professional": "Write in a formal, professional business tone. Be concise, clear, and respectful.",
    "friendly":     "Write in a warm, friendly, and approachable tone while remaining professional.",
    "persuasive":   "Write in a compelling and persuasive tone. Highlight benefits and encourage action.",
    "apologetic":   "Write in a sincere and empathetic tone. Acknowledge the issue and offer resolution.",
    "assertive":    "Write in a confident and direct tone. Be clear about expectations and next steps.",
    "formal":       "Write in a strictly formal tone following business letter conventions.",
}

EMAIL_TYPES = {
    "inquiry":       "a professional inquiry email",
    "follow_up":     "a follow-up email after a meeting or previous communication",
    "proposal":      "a business proposal email",
    "complaint":     "a professional complaint or concern email",
    "thank_you":     "a thank-you email",
    "introduction":  "a self-introduction or company introduction email",
    "meeting":       "a meeting request or scheduling email",
    "rejection":     "a polite rejection email",
    "resignation":   "a professional resignation letter/email",
    "cold_outreach": "a cold outreach / networking email",
}


def build_system_prompt(tone: str, email_type: str) -> str:
    tone_instruction = TONE_PROMPTS.get(tone, TONE_PROMPTS["professional"])
    type_desc = EMAIL_TYPES.get(email_type, "a professional business email")
    return f"""You are an expert business communication specialist and email writing assistant.
Your task is to generate {type_desc}.

Tone guidelines: {tone_instruction}

Rules:
- Always include: Subject line, greeting, body paragraphs, closing, and signature placeholder.
- Format: Use clear paragraph breaks. Start with "Subject: ..." on the first line.
- Keep emails concise but complete — typically 3-5 paragraphs.
- Do NOT include placeholder text like [Name] unless the user hasn't provided the name.
- Make the email ready to send with minimal editing.
- If information is missing, make reasonable professional assumptions.
"""


def build_user_prompt(context: dict) -> str:
    parts = []
    if context.get("sender_name"):
        parts.append(f"Sender: {context['sender_name']}")
    if context.get("sender_role"):
        parts.append(f"Sender's role: {context['sender_role']}")
    if context.get("recipient_name"):
        parts.append(f"Recipient: {context['recipient_name']}")
    if context.get("recipient_role"):
        parts.append(f"Recipient's role: {context['recipient_role']}")
    if context.get("company"):
        parts.append(f"Company: {context['company']}")
    if context.get("key_points"):
        parts.append(f"Key points to cover:\n{context['key_points']}")
    if context.get("additional_info"):
        parts.append(f"Additional context: {context['additional_info']}")

    return "\n".join(parts) + "\n\nPlease generate the complete email now."


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/generate", methods=["POST"])
def generate_email():
    data = request.get_json()

    tone = data.get("tone", "professional")
    email_type = data.get("email_type", "inquiry")
    language = data.get("language", "English")
    context = {
        "sender_name":    data.get("sender_name", ""),
        "sender_role":    data.get("sender_role", ""),
        "recipient_name": data.get("recipient_name", ""),
        "recipient_role": data.get("recipient_role", ""),
        "company":        data.get("company", ""),
        "key_points":     data.get("key_points", ""),
        "additional_info": data.get("additional_info", ""),
    }

    system_prompt = build_system_prompt(tone, email_type)
    if language.lower() != "english":
        system_prompt += f"\n\nIMPORTANT: Write the email in {language}."

    user_prompt = build_user_prompt(context)

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        email_text = completion.choices[0].message.content
        return jsonify({"success": True, "email": email_text})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/refine", methods=["POST"])
def refine_email():
    """Refine/improve an existing email draft."""
    data = request.get_json()
    original_email = data.get("email", "")
    instruction = data.get("instruction", "Make it more concise and professional.")

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert email editor. Refine the given email based on the user's instruction. Return only the refined email, no commentary.",
                },
                {
                    "role": "user",
                    "content": f"Original email:\n\n{original_email}\n\nInstruction: {instruction}\n\nProvide the refined email:",
                },
            ],
            temperature=0.6,
            max_tokens=1024,
        )
        refined = completion.choices[0].message.content
        return jsonify({"success": True, "email": refined})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/suggest-subject", methods=["POST"])
def suggest_subject():
    """Suggest alternative subject lines for an email."""
    data = request.get_json()
    email_body = data.get("email", "")

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an email subject line expert. Generate 5 compelling subject line alternatives for the given email. Return only a JSON array of strings.",
                },
                {
                    "role": "user",
                    "content": f"Email:\n\n{email_body}\n\nGenerate 5 subject line alternatives as a JSON array:",
                },
            ],
            temperature=0.8,
            max_tokens=200,
        )
        raw = completion.choices[0].message.content.strip()
        # Extract JSON array from response
        start = raw.find("[")
        end = raw.rfind("]") + 1
        if start != -1 and end > start:
            subjects = json.loads(raw[start:end])
        else:
            subjects = [raw]
        return jsonify({"success": True, "subjects": subjects})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/analyze-tone", methods=["POST"])
def analyze_tone():
    """Analyze the tone and professionalism of an email."""
    data = request.get_json()
    email_text = data.get("email", "")

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """Analyze the email and return a JSON object with these fields:
{
  "tone": "detected tone (e.g., formal, friendly, aggressive, passive)",
  "professionalism_score": 1-10,
  "clarity_score": 1-10,
  "persuasiveness_score": 1-10,
  "strengths": ["list of strengths"],
  "improvements": ["list of suggested improvements"],
  "overall_rating": "Excellent/Good/Fair/Needs Work"
}
Return only valid JSON.""",
                },
                {
                    "role": "user",
                    "content": f"Analyze this email:\n\n{email_text}",
                },
            ],
            temperature=0.3,
            max_tokens=500,
        )
        raw = completion.choices[0].message.content.strip()
        start = raw.find("{")
        end = raw.rfind("}") + 1
        analysis = json.loads(raw[start:end])
        return jsonify({"success": True, "analysis": analysis})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
