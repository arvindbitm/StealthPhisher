import google.generativeai as genai
import re
import json
from urllib.parse import urlparse

# Configure GenAI API Key
genai.configure(api_key="AIzaSyA0xEUjMpuMO1WaU_RuVSqFKoDFvF7BErM")

def prediction_with_genai(url, features, data):
    report_input = f"""
    Given the following URL and its features, classify it as "Phishing" or "Benign".
    Also, provide a probability score (between 0% and 100%) for each class.

    URL: {url}
    Features: {features}
    Data: {data}

    Expected format:
    Classification: <Phishing or Benign>
    Phishing Probability: <percentage>
    Benign Probability: <percentage>
    """

    try:
        genai_model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config={"temperature": 1, "top_p": 1, "top_k": 64, "max_output_tokens": 8192}
        )
        response = genai_model.generate_content([report_input])

        if response and hasattr(response, 'candidates') and len(response.candidates) > 0:
            generated_text = response.candidates[0].content.parts[0].text.strip()
            
            match = re.search(r"Classification:\s*(Phishing|Benign)", generated_text)
            phishing_prob_match = re.search(r"Phishing Probability:\s*([\d.]+)%", generated_text)
            benign_prob_match = re.search(r"Benign Probability:\s*([\d.]+)%", generated_text)

            classification = match.group(1) if match else "Unknown"
            phishing_probability = float(phishing_prob_match.group(1)) if phishing_prob_match else 0.0
            benign_probability = float(benign_prob_match.group(1)) if benign_prob_match else 0.0

            return classification, phishing_probability, benign_probability
        
        return "No response", 0.0, 0.0

    except Exception as e:
        return f"GenAI analysis failed: {e}", 0.0, 0.0
