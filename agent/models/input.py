from abc import ABC
from dataclasses import dataclass
from typing import List, TypeVar

from chromadb import Where

from agent.models.file import File
from agent.models.issue import Issue

class InputBase(ABC): pass

InT = TypeVar("InT", bound=InputBase)

@dataclass
class QueryFormatterInput(InputBase):
    issue: Issue
    
@dataclass
class FileInput(InputBase):
    files: List[File] 
    
@dataclass
class EmbeddingModelInput(InputBase):
    queries: List[str]
    conditionals: List[Where]
    