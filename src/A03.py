from pydantic import BaseModel, Field
from tools import json_to_xml
from Header import HEADER
import random
import datetime
    
class A03Data(BaseModel):
    SourcePlant: str = Field (default = "D100")
    DestinationPlant: str = Field (default = "P150")
    MaterialCode: str = Field('1000181')
    ControlNo: str = Field(default_factory=lambda: f"{datetime.datetime.now().strftime('%y%m%d')}{random.randint(1000, 9999)}")
    GRTF_Quantity: str = Field('1000.000')
    QMNo_ofContainers: str = Field('10')
    Quantity: str = Field('100.000')
    UOM: str = Field('kg')
    SourceLocation: str = Field('5111')
    TargetLocation: str = Field('D521')
    TransferOrderNo: str = Field("")
    TransferOrderItemNo: str = Field('1')
    ExpiryDate: str = Field('20261231')
    DeletionFlag: str = Field(default="")

class A03(BaseModel):
    #TransferOrderNo: str = Field(default_factory=lambda:random.randint(1000000, 9999999), description="Transfer Order Number")
    Header: HEADER = Field(...)
    DataS: list[A03Data] = Field(...)
    def to_xml(self):
        return json_to_xml(self.model_dump(), root_name="TransactionRequest")

if __name__ == "__main__":
    a3_example = A03(
        Header=HEADER(TransactionType="A03"),
        DataS=[
            A03Data(),
            A03Data()
        ]
    )
    print(a3_example.to_xml())



