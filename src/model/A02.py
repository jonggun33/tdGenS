from pydantic import BaseModel, Field
from .tools import json_to_xml
from .Header import HEADER

class A02Data(BaseModel):
    MaterialCode: str = Field('1000181', description = "Material Code")
    BatchNo: str = Field('260303999', description = "Batch Number")
    BatchStatus : str = Field('Active', description = "Batch Status")

class A02(BaseModel):
    Header: HEADER = Field(..., description="A2 Header Information")
    DataS: list[A02Data] = Field(..., description="List of A2 Data Records")
    def to_xml(self):
        return json_to_xml(self.model_dump(), root_name="TransactionRequest")