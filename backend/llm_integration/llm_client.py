import groq
import json
import re

class GroqClient:
    def __init__(self, api_key):
        self.client = groq.Groq(api_key=api_key)

    def generate_text(self, prompt):
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": self._generate_groq_prompt(prompt),
                    }
                ],
                model="deepseek-r1-distill-llama-70b",
            )
            response = chat_completion.choices[0].message.content
            print("Raw Groq API Response:")
            print(response)
            return self._parse_groq_response(response)

        except Exception as e:
            print(f"Error during Groq API call: {e}")
            return {}

    def _generate_groq_prompt(self, prompt):

     return f"""
        You are a highly creative and artistic image editing expert. Your goal is to transform user prompts into visually compelling and **noticeably impactful** image adjustments in STRICT JSON format.

        **JSON Format Requirements:**

        * All property names (keys) MUST be enclosed in double quotes.
        * Adhere to the following JSON structure:

            {{
                "edits": [
                    {{
                        "target_area": "<string>", // "object", "background", or "global"
                        "brightness": <float>, // 0.6 to 1.4, default 1.0
                        "contrast": <float>, // 0.6 to 1.4, default 1.0
                        // ... other parameters ONLY from the list provided below ...
                    }},
                    // ... more edit objects if needed ...
                ]
            }}

        **Allowed Parameters (STRICTLY USE ONLY THESE. NO OTHER PARAMETERS ALLOWED):**
        brightness (0.2-2.0), contrast (0.2-2.0), saturation (0.0-3.0), hue (-0.5-0.5), angle (-180-180), width (positive int), height (positive int), sharpen (true/false), blur (true/false), invert (true/false), grayscale (true/false), red_factor (0.5-2.0), green_factor (0.5-2.0), blue_factor (0.5-2.0), exposure (0.2-2.0), vignette (0.0-1.0), noise (0-50), black_point (0-100), white_point (155-255), midtones (0.5-2.0), red_r (-1.0-2.0), red_g (-1.0-2.0), red_b (-1.0-2.0), green_r (-1.0-2.0), green_g (-1.0-2.0), green_b (-1.0-2.0), blue_r (-1.0-2.0), blue_g (-1.0-2.0), blue_b (-1.0-2.0), red_tint (-50-50), green_tint (-50-50), blue_tint (-50-50)

        **Important:** DO NOT invent or use any parameters that are not in the "Allowed Parameters" list.

        **Understanding User Prompts:**

        1.  **Identify the Target(s):**
            - "me," "I," "myself": Focus on the primary subject (person/object). "target_area": "object".
            - "background": Edit the background. "target_area": "background".
            - "image," "it," or general requests: Apply edits globally. "target_area": "global".
            - **Multiple Targets:** If the prompt specifies edits for multiple targets (e.g., "me and the background"), return an array of edit objects, each with its own "target_area".
            - **Global Default:** If the user does not mention specific targets like "me" or "background", apply all edits globally. Only create object or background edit objects if the user explicitly asks for them.

        2.  **Interpreting Edit Requests: Subtle yet Creative Enhancements!**
            - When encountering artistic descriptors such as "vintage," "cinematic," or "dreamy," apply **subtle but creative** transformations using relevant parameters like vignette, saturation shifts, contrast tweaks, or slight tint adjustments.
            - Ensure that the effect is **recognizable yet natural**, enhancing the artistic quality rather than drastically altering the image.
            
        3.  **Parameter Ranges: Balanced Yet Impactful Adjustments!**
            - Apply parameters within the allowed range but ensure that the effect remains **visually engaging yet refined**.

        4.  **Strict Rules:**
            - **Only use parameters from the ALLOWED PARAMETERS list.**
            - **Adhere to the JSON format.**
            - **Use default values ONLY for the specified target area. Do not apply defaults to target areas that are not needed.**
            - **If multiple targets are specified, return a JSON array of edit objects.**

        5. **Parameter Check:**
            - After generating the JSON, carefully check that it contains ONLY the parameters from the ALLOWED PARAMETERS list.

        **User Prompt:** '{prompt}'

        **JSON Output:**
    """

    def _repair_json(self, json_string):
        """Repairs JSON strings with missing quotes around keys."""
        repaired_json = re.sub(r'(\s*?)([a-zA-Z_][a-zA-Z0-9_]*?)(:)', r'\1"\2"\3', json_string)
        return repaired_json

    def _validate_response(self, json_response):
        """Validates the JSON response to ensure only allowed parameters are used."""
        allowed_params = {
            "target_area", "brightness", "contrast", "saturation", "hue", "angle", "width", "height", "sharpen", "blur",
            "invert", "grayscale", "red_factor", "green_factor", "blue_factor", "exposure", "vignette", "noise",
            "black_point", "white_point", "midtones", "red_r", "red_g", "red_b", "green_r", "green_g", "green_b",
            "blue_r", "blue_g", "blue_b", "red_tint", "green_tint", "blue_tint"
        }

        if "edits" in json_response:
            for edit in json_response["edits"]:
                for key in list(edit.keys()):
                    if key not in allowed_params:
                        print(f"Error: Invalid parameter '{key}' found in Groq response.")
                        del edit[key]
        return json_response

    def _parse_groq_response(self, response):
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            json_string = json_match.group(0)
            repaired_json_string = self._repair_json(json_string)
            try:
                json_response = json.loads(repaired_json_string)
                validated_response = self._validate_response(json_response)
                if "edits" not in validated_response:
                    validated_response = {"edits": [self._complete_adjustment_factors(validated_response)]}
                else:
                    for edit in validated_response["edits"]:
                        self._complete_adjustment_factors(edit)
                return validated_response
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return {}
        else:
            print("JSON not found in Groq response.")
            return {}

    def _complete_adjustment_factors(self, adjustment_factors):
        """Completes missing adjustment factors with default values."""
        defaults = {
            'target_area': "object",
            'brightness': 1.0,
            'contrast': 1.0,
            'saturation': 1.0,
            'hue': 0.0,
            'angle': 0,
            'width': None,
            'height': None,
            'sharpen': False,
            'blur': False,
            'invert': False,
            'grayscale': False,
            'red_factor': 1.0,
            'green_factor': 1.0,
            'blue_factor': 1.0,
            'exposure': 1.0,
            'vignette': 0.0,
            'noise': 0,
            'black_point': 0,
            'white_point': 255,
            'midtones': 1.0,
            'red_r': 1.0,
            'red_g': 0.0,
            'red_b': 0.0,
            'green_r': 0.0,
            'green_g': 1.0,
            'green_b': 0.0,
            'blue_r': 0.0,
            'blue_g': 0.0,
            'blue_b': 1.0,
            'red_tint': 0,
            'green_tint': 0,
            'blue_tint': 0,
        }

        for key, value in defaults.items():
            if key not in adjustment_factors:
                adjustment_factors[key] = value

        return adjustment_factors










