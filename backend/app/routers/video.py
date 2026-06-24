from fastapi import APIRouter
from pydantic import BaseModel
from app.tasks.video_tasks import generate_video_task
from celery.result import AsyncResult
from app.services.trend_scraper import get_trending_topics

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

@router.get("/trending-topics/{niche}")
async def get_trending(niche: str = "teknologi"):
    topics = get_trending_topics(niche)
    return {
        "niche": niche,
        "count": len(topics),
        "topics": topics[:5]
    }

@router.post("/generate-from-trending/{niche}")
async def generate_from_trending(niche: str = "teknologi"):
    """
    Auto-generate video dari topik trending.
    Ambil topik #1 yang trending, buat video langsung.
    """
    topics = get_trending_topics(niche)
    
    if not topics:
        return {"status": "error", "message": "Tidak ada topik trending ditemukan"}
    
    # Pakai topik paling trending (index 0)
    selected_topic = topics[0]["topic"]
    
    task = generate_video_task.delay(
        topic=selected_topic,
        niche=niche
    )
    
    return {
        "status": "processing",
        "job_id": task.id,
        "topic": selected_topic,
        "message": "Video sedang diproses dari topik trending"
    }