from fastapi import FastAPI
from web.routers import games, platforms

app = FastAPI(title="Arcadia Admin")

# Include Routers
app.include_router(games.router)
app.include_router(platforms.router)

@app.get("/")
def read_root():
    return {"status": "Arcadia Admin Online"}

if __name__ == "__main__":
    import uvicorn
    # Run on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)