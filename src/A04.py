from pydantic import BaseModel, Field
from tools import json_to_xml
from Header import HEADER
import random

class Component(BaseModel):
    ReservationItemNo: str=Field("")
    ItemNo:str=Field(default_factory=lambda: str(random.randint(1000, 9999)))
    ComponentCode:str=Field("")
    ComponentUOM:str=Field("G")
    Target:str=Field("100.000")
    StorageLocation:str=Field("D511")
    ValidDecimalPoint:str=Field("")

class A04Data(BaseModel):
    PlantId: str=Field("P150")
    ProductionOrderNo: str=Field(default_factory=lambda: str(random.randint(1000000, 9999999)))
    ProductNo: str=Field("A5OAM")
    BOMBaseQuantity: str=Field("100.000")
    ProductionQuantity: str=Field("100.000")
    ProductUOM: str=Field("L", description="Unit of Measure")
    BatchNo: str=Field(default_factory=lambda: str(random.randint(100000, 999999)))
    BatchStartDateTime: str=Field("20260901000000")
    BatchEndDateTime: str=Field("20260930235959")
    OperationStartDateTime: str=Field("20260901000000")
    OperationEndDateTime: str=Field("20260930235959")
    BOMAlternativeNo: str=Field("11")
    ReservationNo: str=Field(default_factory=lambda: str(random.randint(1000000, 9999999)))
    OperationNo: str=Field(default_factory=lambda: str(random.randint(1000, 9999)))
    OperationDescription: str=Field("Test Operation")
    MBRDocumentNo: str = Field("A5OAM01")
    Components: list[Component] = Field(...)

class A04(BaseModel):
    Header: HEADER = Field(...)
    DataS: list[A04Data] = Field(...)
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
