from pydantic import BaseModel, Field

class HalbLabel(BaseModel):
    consum_id: str = Field(...)
    def __str__(self):
        return f"{self.consum_id}"