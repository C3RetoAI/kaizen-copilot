from enum import Enum
import re
from typing import Optional, Tuple

from agent.models.agentbase import AgentBase
from agent.models.context import Context
from agent.models.embedded_file import EmbeddedFile, Metadata
from agent.models.input import InputBase, QueryFormatterInput
from agent.models.mcpstep import ROLE, MCPStep
from agent.models.output import OutputBase, QueryFormatterOutput

"""
Query formart according to how the files are recorded:
"""

class CodeExtension(Enum):
    python = "py"
    cpp = "cpp"
    csharp = "csharp"
    java = "java"
    javascript = "js"
    typescript = "ts"
    html = "html"
    css = "css"
    json = "json"
    bash = "sh"
    shell = "sh"
    ruby = "rb"
    go = "go"
    rust = "rs"
    php = "php"
    kotlin = "kt"
    swift = "swift"
    sql = "sql"
    yaml = "yaml"
    markdown = "md"

def get_extension(language: str) -> Optional[str]:
    try:
        return CodeExtension[language.lower()].value
    except KeyError:
        return None
    
class QueryFormatter(AgentBase[QueryFormatterInput, QueryFormatterOutput]):
    def __init__(self):
        super().__init__()
        self.agent_name: str = "QueryFormatter"
        self.role: ROLE = ROLE.QUERY_FORMATTER
        self.purpose: str = "Format the issue to solve to create a properly query to find the files"
        pass
    
    def run(self, input_data: QueryFormatterInput, context: Context) -> Tuple[QueryFormatterOutput, Context, int]:
        self.context = context
        issue_description = input_data.issue.description
        self.context.issue = input_data.issue
        # match = re.findall(r"```(?:\s*)(.*?)(?:\s*)```", issue_description, re.DOTALL)
        # description = re.sub(r"```(?:\s*)(.*?)(?:\s*)```", issue_description, re.DOTALL)

        # if match:
        #     code = match.group(1)
            
        #     start, end = match.span()  
        #     outside_text = (issue_description[:start] + issue_description[end:]).strip()  
            
        #     final_string = f"{outside_text}\n{code}"
            
        #     self.context.issue.code_snippets.append(code)
            
        #     return QueryFormatterOutput(queries=[final_string], conditionals=None), self.context, 1
        # else:
        return QueryFormatterOutput(queries=[issue_description], conditionals=None), self.context, 1
