from pydantic import BaseModel, Field
from tools import json_to_xml
from Header import HEADER

class A13Data(BaseModel):
    ReservationNo: str = Field('88888888')
    ReservationItem: str = Field('1')
    Material : str = Field('1001355')
    Quantity : str = Field('20.000')
    UOM : str = Field('KG')
    WBS: str = Field('100100')
    CostCenter: str = Field('DS2000D')
    StorageLocation: str = Field('')   
    ControlNo: str = Field('')
    DateReservation: str = Field('20260404')
    GoodsRecipient: str = Field('abd.def')
    DeletionFlag: str = Field("X")

class A13(BaseModel):
    Header: HEADER = Field(...)
    DataS: list[A13Data] = Field(...)
    def to_xml(self):
        return json_to_xml(self.model_dump(), root_name="TransactionRequest")   
