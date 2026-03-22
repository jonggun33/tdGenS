from pydantic import BaseModel, Field

class MSLabel(BaseModel):
    mat_code: str = Field(..., description="Material code for the label")
    control_no: str = Field(..., description="Control number for the label")
    expiry: str = Field(...)
    label_code : str = Field(...)
    def __str__(self):
        return f"{self.mat_code}_{self.control_no}_{self.expiry}_{self.label_code}"


