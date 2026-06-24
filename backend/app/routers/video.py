from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.script_generator import generate_script
from services.tts_service import generate_audio
from services.footage_fetcher import get_footage_per_segment
from services.video_assembler import assemble_video

router = APIRouter(prefix="/api", tags=["video"])

class VideoRequest(BaseModel):
    topic: str
    niche: str = "teknologi"

class VideoResponse(BaseModel):
    status: str
    title: str
    hashtags: list
    video_url: str

@router.post("/generate-video", response_model=VideoResponse)
async def generate_video(request: VideoRequest):
    import uuid
    job_id = str(uuid.uuid4())[:8]
    output_dir = f"outputs/{job_id}"
    
    # Step 1: Generate script
    script = generate_script(topic=request.topic, niche=request.niche)
    
    # Step 2: Generate audio
    audio_path = generate_audio(
        text=script['full_script'],
        output_path=f"{output_dir}/audio.mp3"
    )
    
    # Step 3: Download footage
    footage_paths = get_footage_per_segment(
        footage_keywords=script['footage_keywords'],
        output_dir=f"{output_dir}/footage"
    )
    
    # Step 4: Assemble video
    video_path = assemble_video(
        footage_paths=footage_paths,
        audio_path=audio_path,
        output_path=f"{output_dir}/final.mp4",
        script_text=script['full_script'],
        target_duration=60
    )
    
    return VideoResponse(
        status="success",
        title=script['title'],
        hashtags=script['hashtags'],
        video_url=f"/outputs/{job_id}/final.mp4"
    )