from pydantic import BaseModel, Field
from tools import json_to_xml
from Header import HEADER

class A02Data(BaseModel):
    BatchNo: str = Field('260303999')
    ExpiryDate : str = Field('2026-03-31')
    BatchStatus : str = Field('Active')
    MaterialCode: str = Field('1000181')

class A02(BaseModel):
    Header: HEADER = Field(...)
    DataS: list[A02Data] = Field(...)
    def to_xml(self):
        return json_to_xml(self.model_dump(), root_name="TransactionRequest")