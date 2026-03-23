from pydantic import BaseModel, Field
from .tools import json_to_xml
from .Header import HEADER
import random

class Component(BaseModel):
    ReservationItemNo: str=Field("", description="Reservation Item Number")
    ItemNo:str=Field(default_factory=lambda: str(random.randint(1000, 9999)), description="Item Number")
    ComponentCode:str=Field("", description="Component Material Code")
    ComponentUOM:str=Field("g", description="Component Unit of Measure")
    Target:str=Field("100.000", description="Target Location")
    StorageLocation:str=Field("D511", description="Storage Location")
    ValidDecimalPoint:str=Field("", description="Valid Decimal Point")

class A04Data(BaseModel):
    ProductionOrderNo: str=Field(default_factory=lambda: str(random.randint(100000, 999999)), description="Production Order Number")
    ProductionQuantity: str=Field("100.000", description="Production Quantity")
    ProductUOM: str=Field("L", description="Unit of Measure")
    BatchNo: str=Field(default_factory=lambda: str(random.randint(100000, 999999)),description="Batch Number")
    BatchStartDateTime: str=Field("20260901", description="Batch Start Date and Time")
    BatchEndDateTime: str=Field("20260930", description="Batch End Date and Time")
    BOMAlternativeNo: str=Field("11", description="BOM Alternative Number")
    ReservationNo: str=Field(default_factory=lambda: str(random.randint(100000, 999999)), description="Reservation Number")
    OperationNo: str=Field(default_factory=lambda: str(random.randint(1000, 9999)), description="Operation Number")
    OperationDescription: str=Field("Test Operation", description="Operation Description")
    MBRDocumentNo: str = Field("A5OAM01", description="MBR Document Number")
    Components: list[Component] = Field(..., description="List of Components")

class A04(BaseModel):
    Header: HEADER = Field(..., description="A4 Header Information")
    DataS: list[A04Data] = Field(..., description="List of A4 Data Records")
    def to_xml(self):
        return json_to_xml(self.model_dump(), root_name="TransactionRequest")

if __name__ == "__main__":
    a4_example = A04(
        Header=HEADER(TransactionType="A04"),
        DataS=[
            A04Data(Components=[Component(), Component()]),
            A04Data(Components=[Component()])
        ]
    )
    print(a4_example.to_xml())
