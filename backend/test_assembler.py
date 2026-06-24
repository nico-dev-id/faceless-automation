import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.script_generator import generate_script
from app.services.tts_service import generate_audio
from app.services.footage_fetcher import get_footage_per_segment
from app.services.video_assembler import assemble_video

if __name__ == "__main__":
    topic = "5 aplikasi AI gratis yang wajib kamu coba sekarang"
    
    print("="*50)
    print("STEP 1: Generate Script")
    print("="*50)
    script = generate_script(topic=topic, niche="teknologi")
    print(f"Judul: {script['title']}")
    print(f"Footage keywords: {script['footage_keywords']}")

    print("\n" + "="*50)
    print("STEP 2: Generate Audio")
    print("="*50)
    audio_path = generate_audio(
        text=script['full_script'],
        output_path="test_output/final/audio.mp3"
    )

    print("\n" + "="*50)
    print("STEP 3: Download Footage Per Segmen")
    print("="*50)
    footage_paths = get_footage_per_segment(
        footage_keywords=script['footage_keywords'],
        output_dir="test_output/final/footage"
    )

    print("\n" + "="*50)
    print("STEP 4: Assemble Video")
    print("="*50)
    final_video = assemble_video(
        footage_paths=footage_paths,
        audio_path=audio_path,
        output_path="test_output/final/output.mp4",
        script_text=script['full_script'],
        target_duration=60
    )

    print("\n" + "="*50)
    print("SELESAI!")
    print("="*50)
    print(f"Video: {final_video}")
    print(f"Judul: {script['title']}")
    print(f"Hashtags: {' '.join(script['hashtags'])}")