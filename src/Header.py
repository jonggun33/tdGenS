from pydantic import BaseModel, Field
import random


class HEADER(BaseModel):
    """Header class shared by A02 and A03"""
    PlantId: str = Field(default="P150", description="Plant ID")
    TransactionId: str = Field(default_factory=lambda: str(random.randint(100000000000, 999999999999)), description="Transaction ID")  # 12 digits
    SourceSystem: str = Field(default="ERP", description="Source System")
    DestinationSystem: str = Field(default="MES", description="Destination System")
    TransactionType: str = Field(description="Transaction Type A02, A03, etc.")
