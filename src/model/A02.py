from pydantic import BaseModel, Field
from .tools import json_to_xml
from .Header import HEADER

class A02Data(BaseModel):
    BatchNo: str = Field('260303999', description = "Batch Number")
    ExpiryDate : str = Field('2026-03-31', description = "Expiry Date")
    BatchStatus : str = Field('Active', description = "Batch Status")
    MaterialCode: str = Field('1000181', description = "Material Code")

class A02(BaseModel):
    Header: HEADER = Field(..., description="A2 Header Information")
    DataS: list[A02Data] = Field(..., description="List of A2 Data Records")
    def to_xml(self):
        return json_to_xml(self.model_dump(), root_name="TransactionRequest")