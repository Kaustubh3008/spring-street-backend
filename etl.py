# import yfinance as yf
# from database import SessionLocal
# import models

# def run_etl_pipeline():
#     print("Starting ETL Pipeline...")
    
#     # Open a database session
#     db = SessionLocal()
    
#     try:
#         # Step 1: Clean the slate (Drop old data so we don't get duplicates if we run this twice)
#         print("Clearing old data...")
#         db.query(models.Holding).delete()
#         db.query(models.SectorExposure).delete()
#         db.query(models.Product).delete()
#         db.commit()

#         # Step 2: Create our flagship product
#         print("Creating Global Growth Prisma product...")
#         prisma = models.Product(
#             name="Global Growth Prisma",
#             description="Diversified exposure to the world's most innovative companies.",
#             cagr="14.2%",
#             min_investment="₹5,00,000",
#             risk_level="High"
#         )
#         db.add(prisma)
#         db.commit()
#         db.refresh(prisma) # Refresh to get the generated ID

#         # Step 3: Define the theoretical portfolio (Tickers and their target weights in the fund)
#         portfolio = {
#             "AAPL": 15.0,  # Apple
#             "MSFT": 12.0,  # Microsoft
#             "NVDA": 10.0,  # Nvidia
#             "ASML": 8.0,   # ASML (European Tech)
#             "NVO": 5.0     # Novo Nordisk (European Healthcare)
#         }

#         sector_weights = {}

#         # Step 4: EXTRACT & TRANSFORM - Fetch live data from Yahoo Finance
#         for ticker, target_weight in portfolio.items():
#             print(f"Fetching live market data for {ticker}...")
#             stock = yf.Ticker(ticker)
#             info = stock.info

#             # Extract the data we need (with fallbacks if Yahoo Finance is missing data)
#             company_name = info.get("shortName", ticker)
#             sector = info.get("sector", "Unknown Sector")

#             # Create the Holding record
#             holding = models.Holding(
#                 product_id=prisma.id,
#                 ticker=ticker,
#                 company_name=company_name,
#                 weight_percentage=target_weight
#             )
#             db.add(holding)

#             # Calculate Sector Exposure dynamically based on the live data
#             if sector in sector_weights:
#                 sector_weights[sector] += target_weight
#             else:
#                 sector_weights[sector] = target_weight

#         # Step 5: LOAD - Save dynamically calculated Sector Exposures to the database
#         print("Saving sector exposures...")
#         for sector_name, weight in sector_weights.items():
#             sector_exposure = models.SectorExposure(
#                 product_id=prisma.id,
#                 sector_name=sector_name,
#                 weight_percentage=weight
#             )
#             db.add(sector_exposure)

#         # Commit all changes to the database
#         db.commit()
#         print("✅ ETL Pipeline completed successfully! Database is fully populated with live data.")

#     except Exception as e:
#         print(f"❌ An error occurred during the ETL process: {e}")
#         db.rollback() # Cancel changes if something breaks
#     finally:
#         db.close() # Always close the database connection

# if __name__ == "__main__":
#     run_etl_pipeline()



import yfinance as yf
from database import SessionLocal
import models
from database import engine

# Rebuild tables so the new ones are created
models.Base.metadata.create_all(bind=engine)

def run_etl_pipeline():
    print("Starting 100% Complete ETL Pipeline...")
    db = SessionLocal()
    
    try:
        # Clear old data
        db.query(models.Holding).delete()
        db.query(models.SectorExposure).delete()
        db.query(models.MarketCapExposure).delete()
        db.query(models.RegionExposure).delete()
        db.query(models.Product).delete()
        db.commit()

        # Create Product
        prisma = models.Product(
            name="Global Growth Prisma",
            description="Diversified exposure to the world's most innovative companies.",
            cagr="14.2%",
            min_investment="₹5,00,000",
            risk_level="High"
        )
        db.add(prisma)
        db.commit()
        db.refresh(prisma)

        portfolio = {"AAPL": 15.0, "MSFT": 12.0, "NVDA": 10.0, "ASML": 8.0, "NVO": 5.0}
        
        # Dictionaries to track weights
        sector_weights = {}
        market_cap_weights = {}
        region_weights = {}

        # EXTRACT & TRANSFORM
        for ticker, weight in portfolio.items():
            print(f"Fetching live data for {ticker}...")
            stock = yf.Ticker(ticker)
            info = stock.info

            # 1. Holdings
            db.add(models.Holding(
                product_id=prisma.id,
                ticker=ticker,
                company_name=info.get("shortName", ticker),
                weight_percentage=weight
            ))

            # 2. Sector Exposure
            sector = info.get("sector", "Unknown Sector")
            sector_weights[sector] = sector_weights.get(sector, 0) + weight

            # 3. Market Cap Exposure Logic (Mega > $200B, Large > $10B)
            cap = info.get("marketCap", 0)
            if cap > 200_000_000_000:
                cap_category = "Mega Cap"
            elif cap > 10_000_000_000:
                cap_category = "Large Cap"
            else:
                cap_category = "Mid/Small Cap"
            
            market_cap_weights[cap_category] = market_cap_weights.get(cap_category, 0) + weight

            # 4. Region/Country Exposure
            country = info.get("country", "Unknown")
            region_weights[country] = region_weights.get(country, 0) + weight

        # LOAD (Save all exposures to DB)
        print("Saving calculated datasets...")
        for name, wt in sector_weights.items(): db.add(models.SectorExposure(product_id=prisma.id, sector_name=name, weight_percentage=wt))
        for name, wt in market_cap_weights.items(): db.add(models.MarketCapExposure(product_id=prisma.id, category=name, weight_percentage=wt))
        for name, wt in region_weights.items(): db.add(models.RegionExposure(product_id=prisma.id, region=name, weight_percentage=wt))

        db.commit()
        print("✅ ETL Pipeline completed! All 4 datasets populated successfully.")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    run_etl_pipeline()