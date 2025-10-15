import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Preferred models in order of quality and context length
PREFERRED_MODELS = [
    "mixtral-8x7b-32768",        # 🧠 32k context window, long + detailed
    "llama-3.1-70b-versatile",   # high reasoning, balanced output
    "llama-3.1-8b-instant",      # fast fallback
]

def analyze_symptoms(symptom_text: str):
    prompt = (
        "Based on these symptoms, suggest possible conditions and next steps "
        "with an educational disclaimer.\n\nSymptoms:\n" + symptom_text
    )

    for model in PREFERRED_MODELS:
        try:
            print(f"🧠 Trying model: {model}")

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a healthcare assistant that provides helpful, "
                            "educational (non-diagnostic) information. "
                            "Always include a disclaimer reminding users to consult medical professionals."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=800,  # give room for longer lists
            )

            print(f"✅ Successfully used: {model}")
            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"⚠️  {model} failed → {e}")

    # fallback if all models fail
    return (
        "Sorry, all models failed to respond. "
        "Please check your Groq API key or try again later."
    )
