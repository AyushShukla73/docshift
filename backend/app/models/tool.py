from typing import List
from pydantic import BaseModel


class ToolDefinition(BaseModel):
    id: str
    label: str
    description: str = ""
    category: str = ""
    supported_inputs: List[str]
    output_type: str
    multi_file: bool = False
    configurable: bool = False