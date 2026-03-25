from pydantic import BaseModel, Field
from tools import json_to_xml
from Header import HEADER

class A13Data(BaseModel):
    ReservationNo: str = Field('88888888', description="Reservation Number")
    ReservationItem: str = Field('1', description="Reservation Item")
    Material : str = Field('1001355', description="Material Code")
    Quantity : str = Field('20.000', description="Quantity")
    UOM : str = Field('KG', description="Unit of Measure")
    WBS: str = Field('100100', description="WBS Element")
    CostCenter: str = Field('DS2000D', description="Cost Center")
    StorageLocation: str = Field('', description="Storage Location")   
    ControlNo: str = Field('', description="Control Number")
    DateReservation: str = Field('20260404', description="Date of Reservation")
    GoodsRecipient: str = Field('abd.def', description="Goods Receipt Date")
    DeletionFlag: str = Field("X", description="Deletion Flag")

class A13(BaseModel):
    Header: HEADER = Field(..., description="A13 Header Information")
    DataS: list[A13Data] = Field(..., description="List of A13 Data Records")
    def to_xml(self):
        return json_to_xml(self.model_dump(), root_name="TransactionRequest")   
