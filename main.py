# Complete FastAPI backend supporting YouTube & Instagram download
# with cookie support, CORS, proxy, and suitable for Railway deployment.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import os
import random

app = FastAPI()

# Allow CORS from all origins (or replace with your domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with ['https://yourdomain.com']
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class DownloadRequest(BaseModel):
    url: str
    format: str  # "mp4" or "mp3"

# Optional free proxies (you can comment this out if not needed)
PROXIES = [
    "142.93.162.127:3128",
    "64.225.8.107:9981",
    "159.203.61.169:8080",
    "51.222.13.193:10084",
    "45.77.157.167:3128"
]

@app.post("/download")
async def download_media(req: DownloadRequest):
    url = req.url
    fmt = req.format.lower()
    output_path = "downloads/%(title)s.%(ext)s"

    cmd = ["yt-dlp", "-o", output_path]

    proxy = random.choice(PROXIES)
    cmd += ["--proxy", f"http://{proxy}"]

    if fmt == "mp3":
        cmd += ["-x", "--audio-format", "mp3"]
    else:
        cmd += ["-f", "best"]

    if "youtube.com" in url or "youtu.be" in url:
        if os.path.exists("youtube_cookies.txt"):
            cmd += ["--cookies", "youtube_cookies.txt"]

    cmd.append(url)

    try:
        subprocess.run(cmd, check=True)
        return {"success": True, "message": "Download completed", "proxy": proxy}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": str(e), "proxy": proxy}
