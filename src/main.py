from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.database import init_db
from src.logic import (
    is_valid_url, generate_short_code, save_url, 
    get_long_url, increment_click, get_stats
)
import os

app = FastAPI(title="URL Shortener API")

# Jalankan init DB saat startup
init_db()

# Pastikan folder static ada
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

class URLRequest(BaseModel):
    long_url: str

@app.get("/")
def read_index():
    return FileResponse('static/index.html')

@app.post("/api/shorten")
def shorten_url(request: URLRequest):
    if not is_valid_url(request.long_url):
        raise HTTPException(status_code=400, detail="Invalid URL format")
    
    short_code = generate_short_code()
    success = save_url(request.long_url, short_code)
    
    if not success:
        raise HTTPException(status_code=500, detail="Database error")
        
    return {"short_code": short_code, "short_url": f"http://localhost:8000/{short_code}"}

@app.get("/{short_code}")
def redirect_to_url(short_code: str):
    long_url = get_long_url(short_code)
    if not long_url:
        raise HTTPException(status_code=404, detail="URL not found")
        
    increment_click(short_code)
    return RedirectResponse(url=long_url)

@app.get("/api/stats/{short_code}")
def url_stats(short_code: str):
    stats = get_stats(short_code)
    if not stats:
        raise HTTPException(status_code=404, detail="URL not found")
    return stats