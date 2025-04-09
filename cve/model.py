"""This module is used to interact with the Gemini model."""
import json
import os
from dotenv import dotenv_values

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Load environment config
DIR = os.path.dirname(os.path.realpath(__file__))
ENV_PATH = os.path.abspath(os.path.join(DIR, '..', '..', '.env.development.local','.env'))
config = dotenv_values(ENV_PATH)
API_KEY = ""

# Gemini generation config
GENERATION_CONFIG = {
    "temperature": 2,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

# Model initialization
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    generation_config=GENERATION_CONFIG,
    google_api_key=API_KEY,  # ✅ correct key
)


# Output parser
# parser = JsonOutputParser(pydantic_object=Response)

# Stateless prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a security assistant helping identify the safest patch version for a library affected by a CVE.\n"
            "Always respond with valid JSON in this format:\n"
            "{{\n"
            "  \"fixed_version\": \"\",\n"
            "  \"justification\": \"\"\n"
            "}}\n"
            "- The 'fixed_version' should be the highest version within the same minor version family (e.g., 6.0.x) that is NOT vulnerable to the given CVE.\n"
            "- The 'justification' must explain why the version is considered safe (e.g., mentioned as fixed in advisory or absent from the affected versions).\n"
            "- If no safe version can be found within the same minor version family, return an empty string for 'fixed_version' and explain that no fixed version was found in 'justification'.\n"
            "- Do NOT suggest upgrading to a different minor or major version (e.g., 6.1.x or 7.0.0 if the affected version is 6.0.2).\n"
            "- Do NOT include any text outside the JSON format."
        ),
        ("user", "{input}")
    ]
)


# Stateless chain: prompt → model → parser
chain = prompt | model 

# Main interaction function
def get_ai_response(question):
    """Get a response from the Gemini model."""
    try:
        response = chain.invoke({"input": question})
        return response

    except json.JSONDecodeError as e:
        print("Error parsing response as JSON.")
        raise ValueError("Received invalid JSON format from the model.") from e

    except Exception as e:
        print("An error occurred:", e)
        raise e
