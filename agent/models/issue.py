from dataclasses import dataclass
from uuid import UUID


@dataclass
class Issue():
    title: str
    description: str
    repo_url: str