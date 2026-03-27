from pydantic import BaseModel


class SourceOut(BaseModel):
    name: str
    type: str
    url: str
    category_default: str
    weight: float
