from fastapi import APIRouter
from pydantic import BaseModel
from app.tasks.video_tasks import generate_video_task
from celery.result import AsyncResult

router = APIRouter(prefix="/api", tags=["video"])

class VideoRequest(BaseModel):
    topic: str
    niche: str = "teknologi"

@router.post("/generate-video")
async def generate_video(request: VideoRequest):
    task = generate_video_task.delay(
        topic=request.topic,
        niche=request.niche
    )
    return {
        "status": "processing",
        "job_id": task.id,
        "message": "Video sedang diproses di background"
    }

@router.get("/job-status/{job_id}")
async def get_job_status(job_id: str):
    task = AsyncResult(job_id)
    
    if task.state == "PENDING":
        return {"status": "pending", "step": "Menunggu diproses..."}
    
    elif task.state == "PROGRESS":
        return {"status": "processing", "step": task.info.get("step", "")}
    
    elif task.state == "SUCCESS":
        result = task.result
        return {
            "status": "success",
            "title": result["title"],
            "hashtags": result["hashtags"],
            "video_url": result["video_url"]
        }
    
    elif task.state == "FAILURE":
        return {"status": "failed", "error": str(task.info)}
    
    return {"status": task.state}