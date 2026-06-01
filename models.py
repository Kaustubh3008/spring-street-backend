# from sqlalchemy import Column, Integer, String, Float, ForeignKey
# from sqlalchemy.orm import relationship
# from database import Base

# class Product(Base):
#     __tablename__ = "products"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)           # e.g., "Global Growth Prisma"
#     description = Column(String)
#     cagr = Column(String)                       # e.g., "14.2%"
#     min_investment = Column(String)             # e.g., "₹5,00,000"
#     risk_level = Column(String)                 # e.g., "High"

#     # Relationships to link this product to its underlying data
#     holdings = relationship("Holding", back_populates="product")
#     sectors = relationship("SectorExposure", back_populates="product")

# class Holding(Base):
#     __tablename__ = "holdings"

#     id = Column(Integer, primary_key=True, index=True)
#     product_id = Column(Integer, ForeignKey("products.id"))
#     ticker = Column(String, index=True)         # e.g., "AAPL"
#     company_name = Column(String)               # e.g., "Apple Inc."
#     weight_percentage = Column(Float)           # e.g., 5.2 (meaning 5.2%)

#     product = relationship("Product", back_populates="holdings")

# class SectorExposure(Base):
#     __tablename__ = "sector_exposures"

#     id = Column(Integer, primary_key=True, index=True)
#     product_id = Column(Integer, ForeignKey("products.id"))
#     sector_name = Column(String)                # e.g., "Technology"
#     weight_percentage = Column(Float)           # e.g., 35.5

#     product = relationship("Product", back_populates="sectors")


from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    cagr = Column(String)
    min_investment = Column(String)
    risk_level = Column(String)

    # All relationships linked dynamically
    holdings = relationship("Holding", back_populates="product")
    sectors = relationship("SectorExposure", back_populates="product")
    market_caps = relationship("MarketCapExposure", back_populates="product")
    regions = relationship("RegionExposure", back_populates="product")

class Holding(Base):
    __tablename__ = "holdings"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    ticker = Column(String, index=True)
    company_name = Column(String)
    weight_percentage = Column(Float)
    product = relationship("Product", back_populates="holdings")

class SectorExposure(Base):
    __tablename__ = "sector_exposures"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    sector_name = Column(String)
    weight_percentage = Column(Float)
    product = relationship("Product", back_populates="sectors")

# --- NEW TABLES BELOW ---

class MarketCapExposure(Base):
    __tablename__ = "market_cap_exposures"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    category = Column(String)  # e.g., "Mega Cap"
    weight_percentage = Column(Float)
    product = relationship("Product", back_populates="market_caps")

class RegionExposure(Base):
    __tablename__ = "region_exposures"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    region = Column(String)    # e.g., "United States"
    weight_percentage = Column(Float)
    product = relationship("Product", back_populates="regions")