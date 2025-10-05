from google import genai
import json

# ⚠️ Hardcoding API keys is unsafe in production.
client = genai.Client(api_key=" <api_key> ")

def analyze_with_ai(data, model_name="gemini-2.5-flash"):
    """Sends collected data to Gemini for phishing risk analysis and report generation."""

    # Convert input data into JSON string for the prompt
    try:
        data_json = json.dumps(data, indent=2)
    except TypeError:
        data_json = str(data)

    # Prompt for structured phishing analysis
    report_input = f"""
--- DATA ---
{data_json}
--- END DATA ---

Analyse provided data on given url.
generate report based on the data in given format:
WhoIS Details Extractor: Retrieves essential domain registration details, such as renewal dates and registrar information,
to assess legitimacy.
Server Details Extractor: This tool provides critical serverrelated information, including server type, IP address, and status codes, to support detailed analysis.
IP Location: This function gathers geographical details
about the IP address, such as country, city, and ISP, helping
to detect anomalies.

investigate on all these; also check the site for input fields, favicons as extras.
do not bold any characters. keep things such that even non techy get the idea of what's happening.

Specify specially whether phishing or benign.

"""

    try:
        response = client.models.generate_content(
            model=model_name,  # Default: gemini-2.5-flash
            contents=report_input,
            config={
                "temperature": 0.7,
                "top_p": 1,
                "top_k": 64,
                "max_output_tokens": 8192,
            },
        )

        # First, try direct text
        if hasattr(response, "text") and response.text:
            return response.text

        # Fallback: extract from candidates
        if hasattr(response, "candidates"):
            parts = []
            for c in response.candidates:
                if hasattr(c, "content") and c.content.parts:
                    for p in c.content.parts:
                        if hasattr(p, "text"):
                            parts.append(p.text)
            if parts:
                return "\n".join(parts)

        return "AI could not generate a report."

    except Exception as e:
        print(f"Error during AI analysis: {e}")
        return "AI analysis failed."
