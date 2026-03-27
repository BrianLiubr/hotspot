from pydantic import BaseModel


class RefreshResponse(BaseModel):
    ok: bool
    message: str
    count: int | None = None
