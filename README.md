# AI-Powered Email Assistant


A beautiful, full-featured web app that generates professional email drafts instantly using the **Groq API**.

---

## Features

| Feature | Description |
|---|---|
|  **AI Email Generation** | Generate professional emails from bullet points |
|  **6 Tone Options** | Professional, Friendly, Persuasive, Apologetic, Assertive, Formal |
|  **10 Email Types** | Inquiry, Follow-up, Proposal, Complaint, Thank You, Introduction, Meeting, Rejection, Resignation, Cold Outreach |
|  **Multi-language** | English, Urdu, French, Spanish, German, Arabic, Chinese, Hindi |
|  **AI Refine** | Improve your email with a custom instruction |
|  **Tone Analyzer** | Professionalism, Clarity, Persuasiveness scores + feedback |
|  **Subject Suggester** | 5 alternative subject lines |
|  **In-browser Editing** | Edit the generated email directly |
|  **Copy to Clipboard** | One-click copy |

---

## Free API Used: Groq

| Provider | Free Tier | Model Used |
|---|---|---|
| **Groq** | Free, generous limits | `llama-3.3-70b-versatile` |

### Get your Free Groq API Key:
1. Go to **https://console.groq.com**
2. Sign up (free, no credit card)
3. Go to **API Keys** → Create key
4. Copy the key

---

##  Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add your API key
Open `.env` and replace:
```
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run the app
```bash
python app.py
```

### 4. Open in browser
```
http://localhost:5000
```

---

##  Project Structure

```
Ai_Email_Ass/
├── app.py              # Flask backend + Groq API integration
├── .env                # API key configuration
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── templates/
    └── index.html      # Frontend (HTML + CSS + JS)
```

---

##  Alternative Free APIs

If you want to switch APIs:

| API | How to switch |
|---|---|
| **Gemini Flash** | `pip install google-generativeai` · Replace client in app.py |
| **Mistral AI** | Same OpenAI-compatible format, just change base_url |
| **Hugging Face** | Use `InferenceClient` |

---

##  Tips for Best Results

- Fill in **Key Points** with specific bullet points — the more detail, the better the email
- Use **Refine** to ask for changes like *"Make it shorter"* or *"Add more urgency"*
- Try **Analyze Tone** to get a quality score before sending
- Use **Suggest Subjects** to pick the best subject line

---

*Built with ❤️ using Flask + Groq API*
