import re
import requests
from agent.models.agentbase import AgentBase
from agent.models.context import Context
from typing import Tuple

from agent.models.file import FILE_TYPE, File
from agent.models.input import FileInput
from agent.models.output import LLMDeveloperOutput


class LLMDeveloper(AgentBase[FileInput, LLMDeveloperOutput]):
    def __init__(self):
        self.__model_endpoint = "http://localhost:11434/api/generate"
        self.__payload = {"model": "qwen3:4b", "stream": False, "prompt": ""}
        pass
        
    def run(self, input_data: FileInput, context: Context) -> Tuple[LLMDeveloperOutput, Context, int]:
        prompt = self.__format_prompt(input_data.files, context)
        
        self.__payload["prompt"] = prompt
        res = requests.post(self.__model_endpoint, json=self.__payload)
        model_response = res.text
        
        code_match = re.search(r"<code>(.*?)</code>", model_response, re.DOTALL)
        changes_match = re.search(r"<changes>(.*?)</changes>", model_response, re.DOTALL)

        if code_match:
            code = code_match.group(1)
            changes = changes_match.group(1)
        else:
            raise RuntimeError("No code has found <code>...</code>")

        return LLMDeveloperOutput(fixed_code=code, comments=changes)
    
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
        
        prompt = f"""You are a software engineer developer and need to resolve the following issue, give me just the solved code between <code></code> and what changes were made between <changes></changes>:
{issue_desciption}
In this file:
{main_file.name}
{main_file.content}
        
Also you are provided of additional files that can serve as context:
{string_context_files}
"""

        return prompt