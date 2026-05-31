from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)           # e.g., "Global Growth Prisma"
    description = Column(String)
    cagr = Column(String)                       # e.g., "14.2%"
    min_investment = Column(String)             # e.g., "₹5,00,000"
    risk_level = Column(String)                 # e.g., "High"

    # Relationships to link this product to its underlying data
    holdings = relationship("Holding", back_populates="product")
    sectors = relationship("SectorExposure", back_populates="product")

class Holding(Base):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    ticker = Column(String, index=True)         # e.g., "AAPL"
    company_name = Column(String)               # e.g., "Apple Inc."
    weight_percentage = Column(Float)           # e.g., 5.2 (meaning 5.2%)

    product = relationship("Product", back_populates="holdings")

class SectorExposure(Base):
    __tablename__ = "sector_exposures"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    sector_name = Column(String)                # e.g., "Technology"
    weight_percentage = Column(Float)           # e.g., 35.5

    product = relationship("Product", back_populates="sectors")