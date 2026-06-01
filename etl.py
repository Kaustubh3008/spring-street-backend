import yfinance as yf
from database import SessionLocal
import models
from database import engine

# Rebuild tables so the new ones are created
models.Base.metadata.create_all(bind=engine)

def run_etl_pipeline():
    print("Starting Resilient ETL Pipeline...")
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
        
        sector_weights = {}
        market_cap_weights = {}
        region_weights = {}

        # The Fallback Data: If Yahoo blocks us, we use this so the app never breaks!
        fallbacks = {
            "AAPL": {"name": "Apple Inc.", "sector": "Technology", "cap": 2800000000000, "country": "United States"},
            "MSFT": {"name": "Microsoft Corp", "sector": "Technology", "cap": 3100000000000, "country": "United States"},
            "NVDA": {"name": "NVIDIA Corp", "sector": "Technology", "cap": 2200000000000, "country": "United States"},
            "ASML": {"name": "ASML Holding", "sector": "Technology", "cap": 380000000000, "country": "Netherlands"},
            "NVO": {"name": "Novo Nordisk", "sector": "Healthcare", "cap": 550000000000, "country": "Denmark"}
        }

        # EXTRACT & TRANSFORM
        for ticker, weight in portfolio.items():
            print(f"Fetching data for {ticker}...")
            
            # --- THE FIX: Try Yahoo first, fallback if blocked ---
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                # yfinance returns an empty dict or errors if rate limited
                if not info or 'shortName' not in info:
                    raise ValueError("Rate limited by Yahoo")
                
                company_name = info.get("shortName", ticker)
                sector = info.get("sector", "Unknown")
                cap = info.get("marketCap", 0)
                country = info.get("country", "Unknown")
                print(f"✅ Successfully fetched live {ticker} data!")
                
            except Exception as e:
                print(f"⚠️ Yahoo blocked IP for {ticker}. Using secure fallback data.")
                fb = fallbacks.get(ticker)
                company_name = fb["name"]
                sector = fb["sector"]
                cap = fb["cap"]
                country = fb["country"]
            # -----------------------------------------------------

            # 1. Holdings
            db.add(models.Holding(product_id=prisma.id, ticker=ticker, company_name=company_name, weight_percentage=weight))

            # 2. Sector Exposure
            sector_weights[sector] = sector_weights.get(sector, 0) + weight

            # 3. Market Cap Exposure
            if cap > 200_000_000_000:
                cap_category = "Mega Cap"
            elif cap > 10_000_000_000:
                cap_category = "Large Cap"
            else:
                cap_category = "Mid/Small Cap"
            
            market_cap_weights[cap_category] = market_cap_weights.get(cap_category, 0) + weight

            # 4. Region/Country Exposure
            region_weights[country] = region_weights.get(country, 0) + weight

        # LOAD 
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