from pydantic import BaseModel, Field
from tools import json_to_xml
from Header import HEADER

class A13Data(BaseModel):
    ReservationItem: str = Field(..., description="Reservation Item")
    Material : str = Field(..., description="Material Code")
    Quantity : str = Field(..., description="Quantity")
    UOM : str = Field(..., description="Unit of Measure")
    WBS: str = Field(..., description="WBS Element")
    CostCenter: str = Field(..., description="Cost Center")
    StorageLocation: str = Field(..., description="Storage Location")   
    ControlNo: str = Field(..., description="Control Number")
    DateReservation: str = Field(..., description="Date of Reservation")
    GoodsRecipient: str = Field(..., description="Goods Receipt Date")
    DeletionFlag: str = Field( description="Deletion Flag")

class A13(BaseModel):
    Header: HEADER = Field(..., description="A13 Header Information")
    DataS: list[A13Data] = Field(..., description="List of A13 Data Records")
    def to_xml(self):
        return json_to_xml(self.model_dump(), root_name="TransactionRequest")   
