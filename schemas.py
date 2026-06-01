# from pydantic import BaseModel
# from typing import List

# # Schema for an individual holding (e.g., Apple stock)
# class HoldingResponse(BaseModel):
#     ticker: str
#     company_name: str
#     weight_percentage: float

#     class Config:
#         from_attributes = True # Tells Pydantic to read data from our SQLAlchemy models

# # Schema for sector exposure (e.g., Technology: 35%)
# class SectorResponse(BaseModel):
#     sector_name: str
#     weight_percentage: float

#     class Config:
#         from_attributes = True

# # The master schema for the entire Prisma Factsheet
# class ProductResponse(BaseModel):
#     name: str
#     description: str
#     cagr: str
#     min_investment: str
#     risk_level: str
    
#     # Notice how we nest the lists inside the product response!
#     holdings: List[HoldingResponse] = []
#     sectors: List[SectorResponse] = []

#     class Config:
#         from_attributes = True


from pydantic import BaseModel
from typing import List

class HoldingResponse(BaseModel):
    ticker: str
    company_name: str
    weight_percentage: float
    class Config: from_attributes = True

class SectorResponse(BaseModel):
    sector_name: str
    weight_percentage: float
    class Config: from_attributes = True

class MarketCapResponse(BaseModel):
    category: str
    weight_percentage: float
    class Config: from_attributes = True

class RegionResponse(BaseModel):
    region: str
    weight_percentage: float
    class Config: from_attributes = True

class ProductResponse(BaseModel):
    name: str
    description: str
    cagr: str
    min_investment: str
    risk_level: str
    
    # Fully populated data arrays
    holdings: List[HoldingResponse] = []
    sectors: List[SectorResponse] = []
    market_caps: List[MarketCapResponse] = []
    regions: List[RegionResponse] = []

    class Config: from_attributes = True