import json
import time
import google.generativeai as genai

# Configure Gemini with your API key (replace with your actual key securely)
genai.configure(api_key="AIzaSyCcJZBEeSN0PhlNJz2RWcW5esphBb1cwqM")

# Initialize the model globally
model = genai.GenerativeModel("gemini-1.5-flash")



def analyze_code(code_data, max_retries=3, backoff_factor=1):
    json_template = {
        "explanation": "<Brief explanation of what the function does>",
        "issues": ["<List of any performance or security issues found>"]
    }

    results = []
    for file in code_data:
        for fn in file.get("functions", []):
            prompt = f"""
You are a code analysis expert.

Analyze the following Python function and return structured JSON only.

Function Details:
Name: {fn.get('name')}
Arguments: {fn.get('args')}
Docstring: {fn.get('docstring')}

Return JSON with the following format:
{json.dumps(json_template, indent=2)}

Respond with JSON only.
"""
            attempt = 0
            while attempt < max_retries:
                try:
                    print(f"Prompt:\n{prompt}")  # Debug log
                    response = model.generate_content(prompt)
                    text = response.text.strip()
                    print(f"Response:\n{text}")  # Debug log

                    if not text:
                        raise ValueError("Empty response from model")

                    analysis = json.loads(text)
                    fn["analysis"] = analysis
                    break  # Success, exit retry loop

                except (json.JSONDecodeError, ValueError) as e:
                    print(f"JSON parsing error or empty response: {e}")
                    fn["analysis"] = {
                        "explanation": None,
                        "issues": ["Failed to parse response as valid JSON or empty response."]
                    }
                    break  # Don’t retry on JSON errors

                except Exception as e:
                    print(f"Error during analysis (attempt {attempt + 1}): {e}")
                    attempt += 1
                    if attempt == max_retries:
                        fn["analysis"] = {
                            "explanation": None,
                            "issues": [f"Error during analysis after {max_retries} attempts: {str(e)}"]
                        }
                    else:
                        sleep_time = backoff_factor * (2 ** (attempt - 1))
                        print(f"Retrying in {sleep_time} seconds...")
                        time.sleep(sleep_time)

        results.append(file)
    return results
