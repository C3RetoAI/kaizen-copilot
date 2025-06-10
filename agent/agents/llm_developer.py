import os
import re
import requests
from agent.models.agentbase import AgentBase
from agent.models.context import Context
from typing import Optional, Tuple

from agent.models.file import FILE_TYPE, File
from agent.models.input import FileInput
from agent.models.mcpstep import ROLE
from agent.models.output import LLMDeveloperOutput
import anthropic

class LLMDeveloper(AgentBase[FileInput, LLMDeveloperOutput]):
    def __init__(self):
        self.__model_endpoint = "http://localhost:11434/api/generate"
        self.__payload = {"model": "qwen3:14b", "stream": False, "prompt": ""}
        self.context = None
        self.tool = None
        self.role = ROLE.DEVELOPER
        self.purpose = ""
        self.generate_patch = False
        self.__api_key = os.environ.get('ANTHROPIC_KEY')
        self.__enable_context = False
        pass
        
    def run(self, input_data: FileInput, context: Context) -> Tuple[LLMDeveloperOutput, Context, int]:
        self.context = context
        prompt = self.__format_prompt(input_data.files, context)
        
        fixed_code = self.__call_model(self.__api_key, prompt)

        main_file = next((input_files for input_files in input_data.files if input_files.file_type == FILE_TYPE.MAIN_FILE), None)
        
        return LLMDeveloperOutput(fixed_code=fixed_code, path_code=main_file.path, comments=""), self.context, 1
   
    def __call_model(self, api_key: Optional[str], prompt: str) -> str:
        if api_key:
            client = anthropic.Anthropic(
                api_key=api_key,
            )
                
            message = client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=1024,
                system="You are a professional software engineer. Your task is to fix the issue described by the user",
                messages=[
                    {"role": "user", "content": prompt}
                ],
            )
        
            return message.content[0].text
        else:
            self.__payload["prompt"] = prompt
            res = requests.post(self.__model_endpoint, json=self.__payload)
            model_response= res.text
            code = re.search(r"<code>(.*?)</code>", model_response, re.DOTALL)

            if code:
                code = code.group(1)
                return code
            else:
                raise RuntimeError("No code has found <code>...</code>")

    
    def __format_prompt(self, files: list[File], context: Context) -> str:
        main_file = None
        context_files = []
        
        for code_file in files:
            if code_file.file_type == FILE_TYPE.MAIN_FILE:
                main_file = code_file
            else: 
                context_files.append(f"{code_file.name}\n{code_file.content}")
                    
        issue_desciption = context.issue.description
        
        string_context_files = "\n\n".join(context_files)
        
        prompt = f"""
Issue to solve:
{issue_desciption}

Here is the main file where the issue occurs {main_file.name} and need to be fixed:
{main_file.content}
"""

        if string_context_files.strip() and self.__enable_context:
            prompt += f"""
You are also provided with additional context files which may help you resolve the issue:

<context>
{string_context_files}
</context>
"""

        prompt += """
Please return only the corrected code as a full patch file.
Do not include explanations, file names, or formatting tags — only the fixed code.
"""

        return prompt