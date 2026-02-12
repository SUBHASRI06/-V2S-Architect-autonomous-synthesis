import os
import time
from google import genai
from PIL import Image

class V2SAgent:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.model_id = 'gemini-2.5-flash' 

    def analyze_diagram(self, image_path):
        """Phase 1: Generates the technical blueprint JSON WITH Mermaid diagram."""
        img = Image.open(image_path)
        prompt = """
        ACT AS A SENIOR SYSTEM ARCHITECT. Analyze this diagram CAREFULLY.
        
        Identify the domain, ALL components, connections, inputs, outputs, and data flow.
        
        OUTPUT ONLY VALID JSON with these EXACT fields:
        {
          "domain": "Hardware/VLSI/Digital Logic/etc",
          "components": ["Component1", "Component2", "Input", "Output"],
          "files": ["main.v", "testbench.v", "README.md"],
          "summary": "One sentence technical description of the system.",
          "mermaid_code": "graph TD\n  A[Input] --> B[Processor]\n  B --> C[Output]\n\nCreate PRECISE Mermaid matching the ACTUAL image architecture."
        }
        
        The mermaid_code MUST represent the EXACT diagram in the image.
        """
        try:
            response = self.client.models.generate_content(model=self.model_id, contents=[prompt, img])
            if response and response.text:
                return response.text
            return None
        except Exception:
            return None

    def generate_all_code_stream(self, blueprint_json):
        """Phase 2: Synthesizes code with strict markers."""
        time.sleep(2)
        prompt = f"""
        ACT AS AN EXPERT DEVELOPER. Generate code based on: {blueprint_json}
        
        RULES:
        1. Write the REAL source code for ALL files listed.
        2. Format EVERY file exactly like this:
        ---FILE_START: filename.ext---
        [Actual Code Content]
        ---FILE_END---
        """
        return self.client.models.generate_content_stream(model=self.model_id, contents=prompt)

    def generate_readme(self, blueprint, full_code):
        """Phase 3: Final Documentation."""
        time.sleep(1)
        prompt = f"Create a professional README.md for this system: {blueprint}"
        response = self.client.models.generate_content(model=self.model_id, contents=prompt)
        return response.text if response else ""
