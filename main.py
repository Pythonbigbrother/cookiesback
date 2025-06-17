from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import yt_dlp
import os
import uuid

app = FastAPI()

class DownloadRequest(BaseModel):
    url: str
    format: str = "mp4"

@app.post("/download")
async def download_video(data: DownloadRequest):
    try:
        os.makedirs("downloads", exist_ok=True)
        filename = str(uuid.uuid4()) + ".%(ext)s"
        output_path = f"downloads/{filename}"

        ydl_opts = {
            'format': 'best',
            'outtmpl': output_path
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(data.url, download=True)
            downloaded_file = ydl.prepare_filename(info)

        return FileResponse(path=downloaded_file, filename=os.path.basename(downloaded_file), media_type='application/octet-stream')

    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})
