from pydantic import BaseModel, Field
from .tools import json_to_xml
import random
import datetime

class A03Header(BaseModel):
    PlantId: str = Field(default="P150", description="Plant ID")
    TransactionId: int = Field(default_factory=lambda: random.randint(100000, 999999), description="Transaction ID") #6 digits    
    SourceSystem: str = Field(default="ERP", description="Source System")
    DestinationSystem: str = Field(default="MES", description="Destination System")
    TransactionType: str = Field(default="A3", description="Transaction Type")
    
class A03Data(BaseModel):
    SourcePlant: str = Field (default = "D100", description = "Source Plant")
    DestinationPlant: str = Field (default = "P150", description = "Destination Plant")
    MaterialCode: str = Field('1000181', description = "Material Code")
    ControlNo: str = Field(default_factory=lambda: f"{datetime.datetime.now().strftime('%y%m%d')}{random.randint(100, 999)}", description = "Control Number")
    GRFT_Quantity: float = Field(1000.000, description = "GRFT Quantity")
    QMNo_ofContainers: int = Field(10, description = "QM Number of Containers")
    Quantity: float = Field(100, description = "Quantity")
    UOM: str = Field('kg', description = "Unit of Measure")
    SourceLocation: str = Field('5111', description = "Source Location")
    TargetLocation: str = Field('D521', description = "Target Location")
    TransferOrderNo: str = Field("", description = "Transfer Order Number")
    TransferOrderItemNo: int = Field(1, description = "Transfer Order Item Number")
    ExpiryDate: str = Field('20261231', description = "Expiry Date")
    DeletionFlag: str = Field(default="", description = "Deletion Flag")

class A03(BaseModel):
    #TransferOrderNo: str = Field(default_factory=lambda:random.randint(1000000, 9999999), description="Transfer Order Number")
    Header: A03Header = Field(..., description="A3 Header Information")
    DataS: list[A03Data] = Field(..., description="List of A3 Data Records")
    def to_xml(self):
        return json_to_xml(self.model_dump(), root_name="TransactionRequest")

if __name__ == "__main__":
    a3_example = A03(
        Header=A03Header(),
        DataS=[
            A03Data(),
            A03Data()
        ]
    )
    print(a3_example.to_xml())



