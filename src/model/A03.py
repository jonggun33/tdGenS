from pydantic import BaseModel, Field
from tools import json_to_xml

class A03Header(BaseModel):
    PlantId: str = Field(default="P150", description="Plant ID")
    TransactionId: int = Field(..., description="Transaction ID") #6 digits    
    SourceSystem: str = Field(default="ERP", description="Source System")
    DestinationSystem: str = Field(default="MES", description="Destination System")
    TransactionType: str = Field(default="A3", description="Transaction Type")
    
class A03Data(BaseModel):
    SourcePlant: str = Field (default = "D100", description = "Source Plant")
    DestinationPlant: str = Field (default = "P150", description = "Destination Plant")
    MaterialCode: str = Field(..., description = "Material Code")
    ControlNo: str = Field(..., description = "Control Number")
    GRFT_Quantity: float = Field(..., description = "GRFT Quantity")
    QMNo_ofContainers: int = Field(..., description = "QM Number of Containers")
    Quantity: float = Field(..., description = "Quantity")
    UOM: str = Field(..., description = "Unit of Measure")
    SourceLocation: str = Field(..., description = "Source Location")
    TargetLocation: str = Field(..., description = "Target Location")
    TransferOrderNo: str = Field(..., description = "Transfer Order Number")
    TransferOrderItemNo: int = Field(..., description = "Transfer Order Item Number")
    ExpiryDate: str = Field(..., description = "Expiry Date")
    DeletionFlag: str = Field(default="", description = "Deletion Flag")

class A03(BaseModel):
    Header: A03Header = Field(..., description="A3 Header Information")
    DataS: list[A03Data] = Field(..., description="List of A3 Data Records")
    def to_xml(self):
        return json_to_xml(self.model_dump(), root_name="TransactionRequest")

if __name__ == "__main__":
    a3_example = A03(
        Header=A03Header(TransactionId=123456),
        DataS=[
            A03Data(
                MaterialCode="MAT001",
                ControlNo="CTRL001",
                GRFT_Quantity=100.0,
                QMNo_ofContainers=10,
                Quantity=100.0,
                UOM="KG",
                SourceLocation="LOC001",
                TargetLocation="LOC002",
                TransferOrderNo="TO001",
                TransferOrderItemNo=1,
                ExpiryDate="2024-12-31"
            ),
            A03Data(
                MaterialCode="MAT001",
                ControlNo="CTRL001",
                GRFT_Quantity=100.0,
                QMNo_ofContainers=10,
                Quantity=100.0,
                UOM="KG",
                SourceLocation="LOC001",
                TargetLocation="LOC002",
                TransferOrderNo="TO001",
                TransferOrderItemNo=1,
                ExpiryDate="2024-12-31"
            )
        ]
    )
    print(a3_example.to_xml())



