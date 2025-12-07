# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine, Base
from routers import users, books, activity, auth

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Readify API",
    description="A book tracking and reading management API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  
        "http://localhost:3000",  
        "http://localhost:8080", 
        "*"  
    ],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)


app.include_router(auth.router)      
app.include_router(users.router)     
app.include_router(books.router)     
app.include_router(activity.router)  


@app.get("/")
def root():
    """Root endpoint - API health check"""
    return {
        "message": "Readify API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)