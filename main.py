from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize the application
app = FastAPI(
    title="Spring Street Data API",
    description="Backend systems powering the Prisma factsheet experience."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)

@app.get("/api/health")
def health_check():
    return {
        "status": "operational", 
        "service": "Spring Street API",
        "version": "1.0.0"
    }

# --- NEW ENDPOINT BELOW ---

@app.get("/api/products/prisma", response_model=schemas.ProductResponse)
def get_prisma_factsheet(db: Session = Depends(get_db)):
    """
    Fetches the full factsheet data for the Global Growth Prisma product,
    including live sector exposures and holdings.
    """
    # Query the database for the Prisma product
    product = db.query(models.Product).filter(models.Product.name == "Global Growth Prisma").first()
    
    # If the database is empty, throw a clean 404 error
    if not product:
        raise HTTPException(
            status_code=404, 
            detail="Prisma product not found. Have you run the ETL pipeline?"
        )
    
    # Because of our relationships in models.py and schemas.py, 
    # FastAPI automatically fetches and attaches the holdings and sectors!
    return product