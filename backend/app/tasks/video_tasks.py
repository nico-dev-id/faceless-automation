import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.tasks.celery_app import celery_app
from app.services.script_generator import generate_script
from app.services.tts_service import generate_audio
from app.services.footage_fetcher import get_footage_per_segment
from app.services.video_assembler import assemble_video

@celery_app.task(bind=True)
def generate_video_task(self, topic: str, niche: str):
    import uuid
    job_id = self.request.id
    output_dir = f"outputs/{job_id}"

    try:
        # Step 1: Generate script
        self.update_state(state="PROGRESS", meta={"step": "Generating script..."})
        script = generate_script(topic=topic, niche=niche)

        # Step 2: Generate audio
        self.update_state(state="PROGRESS", meta={"step": "Generating audio..."})
        audio_path = generate_audio(
            text=script['full_script'],
            output_path=f"{output_dir}/audio.mp3"
        )

        # Step 3: Download footage
        self.update_state(state="PROGRESS", meta={"step": "Downloading footage..."})
        footage_paths = get_footage_per_segment(
            footage_keywords=script['footage_keywords'],
            output_dir=f"{output_dir}/footage"
        )

        # Step 4: Assemble video
        self.update_state(state="PROGRESS", meta={"step": "Assembling video..."})
        video_path = assemble_video(
            footage_paths=footage_paths,
            audio_path=audio_path,
            output_path=f"{output_dir}/final.mp4",
            script_text=script['full_script'],
            target_duration=60
        )

        return {
            "status": "success",
            "title": script['title'],
            "hashtags": script['hashtags'],
            "video_url": f"/outputs/{job_id}/final.mp4"
        }

    except Exception as e:
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise