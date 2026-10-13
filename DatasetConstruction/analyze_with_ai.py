import google.generativeai as genai
import os
from urllib.parse import urlparse

# Ensure the API key is set up
genai.configure(api_key="AIzaSyA0xEUjMpuMO1WaU_RuVSqFKoDFvF7BErM")

# def save_raw_response(response_text, domain_name):
#     """Save the raw AI response to a text file named after the domain name."""
#     save_dir = "static/gen_reports"
#     os.makedirs(save_dir, exist_ok=True)  # Ensure the directory exists
#     file_path = os.path.join(save_dir, f"{domain_name}.txt")

#     try:
#         with open(file_path, "w", encoding="utf-8") as file:
#             file.write(response_text)
#         print(f"Raw response saved to {file_path}")
#     except Exception as e:
#         print(f"Error saving raw response: {e}")

# def get_domain_name(url):
#     """Extract domain name from URL."""
#     if not url:
#         print("ERROR: No URL provided.")
#         return "Not provided"
    
#     parsed_url = urlparse(url)
#     print(f"DEBUG: Parsed URL -> {parsed_url}")

#     # Handle case where netloc might be empty
#     domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path
#     print(f"DEBUG: Extracted domain -> {domain}")
    
#     # If no domain is extracted, return "Not provided"
#     if not domain:
#         print("ERROR: No domain found in the URL.")
#         return "Not provided"
    
#     # domain_parts = domain.split('.')
#     # domain_name = '.'.join(domain_parts[-2:]) if len(domain_parts) > 2 else domain

#     # print(f"DEBUG: Final domain name -> {domain_name}")
#     return domain

import google.generativeai as genai
import os
from urllib.parse import urlparse

# Ensure the API key is set up
genai.configure(api_key="AIzaSyA0xEUjMpuMO1WaU_RuVSqFKoDFvF7BErM")

def save_raw_response(response_text, domain_name):
    """Save the raw AI response to a text file named after the domain name."""
    save_dir = "static/gen_reports"
    os.makedirs(save_dir, exist_ok=True)  # Ensure the directory exists
    file_path = os.path.join(save_dir, f"{domain_name}.txt")

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(response_text)
        print(f"Raw response saved to {file_path}")
    except Exception as e:
        print(f"Error saving raw response: {e}")

def get_domain_name(url):
    """Extract domain name from URL."""
    if not url:
        print("ERROR: No URL provided.")
        return "Not provided"
    
    parsed_url = urlparse(url)
    print(f"DEBUG: Parsed URL -> {parsed_url}")

    # Handle case where netloc might be empty
    domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path
    print(f"DEBUG: Extracted domain -> {domain}")
    
    # If no domain is extracted, return "Not provided"
    if not domain:
        print("ERROR: No domain found in the URL.")
        return "Not provided"
    
    # domain_parts = domain.split('.')
    # domain_name = '.'.join(domain_parts[-2:]) if len(domain_parts) > 2 else domain

    # print(f"DEBUG: Final domain name -> {domain_name}")
    return domain

def analyze_with_ai(data):
    """Generate a phishing risk analysis report using AI."""
    url = data.get('url', '')
    if not url:
        print("ERROR: URL is missing in the request data.")
        return "URL is missing."

    server_type = data.get('Server_Type', 'Not provided')
    server_version = data.get('Server_Version', 'Not provided')
    x_powered_by = data.get('X_Powered_By', 'Not provided')
    ip_country = data.get('IP_Country', 'Not provided')
    ip_city = data.get('IP_City', 'Not provided')
    whois_status = data.get('WHOIS_Status', 'Not provided')

    print(f"Received URL: {url}")
    
    # Parse the domain name from the URL
    domain_name = get_domain_name(url)
    
    #print(f"Collected data: {data}")
    print(f"DEBUG: Extracted domain name -> {domain_name}")
    
    # Prepare the input for AI model
    report_input = f"""
    Generate a detailed phishing risk analysis report based on the following server details and URL:

    URL: {url}
    Server Type: {server_type}
    Server Version: {server_version}
    X-Powered-By: {x_powered_by}
    IP Country: {ip_country}
    IP City: {ip_city}
    WHOIS Status: {whois_status}

    Please provide the report in the following JSON format:

    {{
        "report": {{
            "1. Initial Observations": {{
                "details": "Detailed observations based on the URL and initial checks.",
                "summary": "Summary of the URL's legitimacy."
            }},
            "2. Analysis of Provided Information": {{
                "analysis": {{
                    "missing_information": "Highlight any missing or suspicious information.",
                    "server_type_analysis": "Analysis of the server type and its implications.",
                    "whois_status_analysis": "Implications of the WHOIS status."
                }},
                "server_details": {{
                    "ip_city": "{ip_city}",
                    "ip_country": "{ip_country}",
                    "server_type": "{server_type}",
                    "server_version": "{server_version}",
                    "whois_status": "{whois_status}",
                    "x_powered_by": "{x_powered_by}"
                }},
                "summary": "Summary of the analysis of provided information."
            }},
            "3. Potential Phishing Risks": {{
                "dns_manipulation": {{
                    "explanation": "Explain the risk of DNS manipulation.",
                    "risk": "Risk level (e.g., Low, Medium, High)."
                }},
                "domain_spoofing": {{
                    "explanation": "Explain the risk of domain spoofing.",
                    "risk": "Risk level (e.g., Low, Medium, High)."
                }},
                "missing_server_details": {{
                    "explanation": "Explain the risks related to missing server details.",
                    "risk": "Risk level (e.g., Low, Medium, High)."
                }},
                "overall_risk_summary": "Overall risk summary.",
                "ssl_concerns": {{
                    "explanation": "Explain the concerns related to SSL.",
                    "risk": "Risk level (e.g., Low, Medium, High)."
                }}
            }},
            "4. Recommendations": {{
                "be_cautious": "Recommendation to be cautious.",
                "dns_checkup": "Recommendation regarding DNS checks.",
                "domain_registration": "Recommendation for checking domain registration.",
                "ssl_verification": "Recommendation for SSL verification.",
                "url_scrutiny": "Recommendation for scrutinizing the URL."
            }},
            "5. Conclusion": {{
                "final_advice": "Final advice based on the analysis.",
                "overall_judgment": "Overall judgment on the site's safety."
            }}
        }}
    }}

    Ensure that each section is filled out appropriately based on the provided details and context and make it highly detailed explained.
    Also make sure to give in the given JSON format only. Do not change the format or keywords like "5. Conclusion" and its sub-keywords like "final_advice", "overall_judgment".
    """

    # Configuration for the generative AI model
    generation_config = {
        "temperature": 1,
        "top_p": 1,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    try:
        # Call to the Generative AI model
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=generation_config,
        )
        response = model.generate_content([report_input])

        if response.text:
            save_raw_response(response.text, domain_name)
            return f"Raw response saved for domain: {domain_name}"
        else:
            return "AI could not generate a response."

    except Exception as e:
        print(f"Error during AI analysis: {e}")
        return f"AI analysis failed: {e}"
