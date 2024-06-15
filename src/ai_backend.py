import json

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dataclasses import dataclass
from history import History

output_schema = {
  "compliant": "number%",
  "name": "string",
  "mobile": ["string"],
  "email": ["string"],
  "companies_worked_for": ["string"],
  "experience_total": "number",
  "experience_relevant": "number",
  "major_tech_stack": ["string"],
  "certifications": ["string"],
  "domains_experience": ["string"]
}

input_schema = {
  "resume-text": "string",
  "jd-text": "string"
}

system_prompt = """
You are ResumeBot, a resume parser that only responds in JSON and that too, STRICTLY COMPLIES with the JSON schema provided

Your inputs:
Resume Text: Resume text that has been parsed from pdf/word document
JD: Job description

The user may/maynot use this INPUT schema
```
{
  "resume-text": "string",
  "jd-text": "string"
}
``` 

However, you MUST ALWAYS USE THIS OUTPUT SCHEMA
```
{
  "compliant": "number%",
  "name": "string",
  "mobile": ["string"],
  "email": ["string"],
  "companies_worked_for": ["string"],
  "experience_total": "number",
  "experience_relevant": "number",
  "major_tech_stack": ["string"],
  "certifications": ["string"],
  "domains_experience": ["string"]
}
```

compliant: How much the candidate is suitable for the provided jd (jd means job description)
name: The full name of candidate (normalise it using "Title Case")
mobile: Any possible mobile numbers of the candidate (No matter how the candidate puts his mobile number, you should always put it as a 10 digit number)
email: Any possible emails of the candidate
companies_worked_for: List of companies he/she worked for
experience_total: Total years of experience
experience_relevant: Years of experience relevant to the jd (job description)
major_tech_stack: Technologies he/she worked with
certifications: Any certifications he/she has (online or otherwise)
domains_experience: Any domain experience he/she has (financial/retail/marketing/it-services)
"""

@dataclass
class AIParser:
    api_key: str
    history_file: str

    def __post_init__(self):
        genai.configure(api_key=self.api_key)

        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        }

        self.history = History(self.history_file)
        self.history.connect()

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=self.generation_config,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            },
            system_instruction=system_prompt,
        )

        self.chat_session = self.model.start_chat(
            history=self.history.dump(),
        )

    @staticmethod
    def sanitize_input(input_ : str):
        # Remove any characters that are not in the utf-8 encoding
        return input_.encode("utf-8", "ignore").decode("utf-8")

    async def parse(self, resume_text: str, jd_text: str) -> dict:
        _resume_json = json.dumps(
            {
                "resume-text": AIParser.sanitize_input(resume_text),
                "jd-text": AIParser.sanitize_input(jd_text)
            }
        )

        response = await self.chat_session.send_message_async(
            _resume_json,
            stream=False,
        )
        self.history.add("user", _resume_json)
        self.history.add("model", response.text)

        self.history.dumpbuffer()
        return json.loads(response.text)


    def close(self):
        self.history.dumpbuffer()
