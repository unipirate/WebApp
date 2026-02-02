import re
import json
from typing import Optional, Dict, Any

from google import genai
from django.conf import settings

class LLMService:
    def __init__(self):
        api_key = getattr(settings, "GEMINI_API_KEY", None)
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in settings.")
        
        self.client = genai.Client(api_key=api_key)

        self.model = getattr(settings, "GEMINI_MODEL_NAME", "gemini-3-flash-preview")

    def generate_regex_pattern(
        self, 
        natural_language: str,
        available_columns: list = None
    ) -> Dict[str, Any]:
        prompt = self._build_prompt(natural_language, available_columns)

        try:
            resp = self.client.models.generate_content(
                model = self.model,
                contents = prompt,
            )

            raw_text = ""
            if hasattr(resp, 'text') and resp.text:
                raw_text = resp.text.strip()
            elif hasattr(resp, 'candidates') and resp.candidates:
                parts = []
                for part in resp.candidates[0].content.parts:
                    if hasattr(part, 'text'):
                        parts.append(part.text)
                raw_text = "".join(parts).strip()
            
            if not raw_text:
                raise ValueError("LLM returned empty response")

            cleaned_text = self._clean_json_response(raw_text)

            try:
                parsed_data = json.loads(cleaned_text)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse JSON from LLM response: {raw_text[:200]}")

            required_fields = ['column_name', 'pattern_description', 'replacement', 'regex_pattern']
            for field in required_fields:
                if field not in parsed_data:
                    raise ValueError(f"LLM response missing required field: {field}")

            column_name = parsed_data['column_name'].strip()
            pattern_description = parsed_data['pattern_description'].strip()
            replacement = parsed_data['replacement'].strip()
            regex_pattern = self._clean_regex_pattern(parsed_data['regex_pattern'])

            if not self._validate_regex(regex_pattern):
                raise ValueError(f"Generated regex pattern is invalid: {regex_pattern}")
            
            if available_columns and column_name not in available_columns:
                column_lower = column_name.lower()
                matched_column = None
                for col in available_columns:
                    if col.lower() == column_lower:
                        matched_column = col
                        break
                
                if matched_column:
                    column_name = matched_column
                else:
                    raise ValueError(
                        f"Column '{column_name}' does not exist. Available columns: {', '.join(available_columns)}"
                    )

            return {
                'column_name': column_name,
                'pattern_description': pattern_description,
                'replacement': replacement,
                'regex_pattern': regex_pattern,
                'model_used': self.model,
                'raw_response': raw_text,
            }
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"LLM service error: {str(e)}")

    def _build_prompt(self, natural_language_input: str, available_columns: list = None) -> str:
        columns_hint = ""
        if available_columns:
            columns_hint = f"Available column names: {', '.join(available_columns)}"
        
        prompt = f"""You are an expert in generating Python regular expressions based on natural language instructions.

User input: "{natural_language_input}"{columns_hint}

Please follow these requirements to parse and generate:

1. Extract from the input:
   - column_name: Target column name (string)
   - pattern_description: Pattern description (string, e.g., "email address", "phone number")
   - replacement: Replacement value (string, without quotes)

2. Based on pattern_description, generate a valid Python regular expression:
   - regex_pattern: Regular expression string (without quotes or code block markers)

3. Return a valid JSON object with the following fields:
   {{
     "column_name": "column name",
     "pattern_description": "pattern description",
     "replacement": "replacement value",
     "regex_pattern": "regular expression"
   }}

Examples 1:
input: "replace all email address in email column to 'REDACTED'"
output:
{{
  "column_name": "email",
  "pattern_description": "email address",
  "replacement": "REDACTED",
  "regex_pattern": "\\\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\\\.[A-Za-z]{{2,7}}\\\\b"
}}

Example 2:
input: "replace the mobile number in phone column to '***'"
output:
{{
  "column_name": "phone",
  "pattern_description": "mobile number",
  "replacement": "***",
  "regex_pattern": "\\\\b\\\\d{{3}}[-.]?\\\\d{{3}}[-.]?\\\\d{{4}}\\\\b"
}}

Example 3:
input: "replace number '4' in name column to 'abcd'"
output:
{{
  "column_name": "name",
  "pattern_description": "number '4'",
  "replacement": "abcd",
  "regex_pattern": "4"
}}

Please provide the JSON response only, without any additional text or explanation.:
input: "{natural_language_input}"
output:"""
        
        return prompt
    
    def _clean_json_response(self, text: str) -> str:
        text = re.sub(r'^```(?:json)?\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'```\s*$', '', text)
        
        text = text.strip()
        
        return text

    def _clean_regex_pattern(self, pattern: str) -> str:
        pattern = re.sub(
            r'^```(?:python|regex)?\s*', 
            '', 
            pattern, 
            flags=re.IGNORECASE
        )
        pattern = re.sub(r'```\s*$', '', pattern)
        pattern = pattern.strip('"\'`')
        pattern = pattern.strip()

        return pattern

    def _validate_regex(self, pattern: str) -> bool:
        try:
            re.compile(pattern)
            return True
        except re.error:
            return False
        