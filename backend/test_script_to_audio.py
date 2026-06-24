import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.script_generator import generate_script
from app.services.tts_service import generate_audio

if __name__ == "__main__":
    print("Step 1: Generate script...")
    script = generate_script(
        topic="5 aplikasi AI gratis yang wajib kamu coba sekarang",
        niche="teknologi"
    )
    
    print(f"Judul: {script['title']}")
    print(f"Script preview: {script['full_script'][:100]}...")
    
    print("\nStep 2: Convert script ke audio...")
    audio_path = generate_audio(
        text=script['full_script'],
        output_path="test_output/script_audio.mp3"
    )
    
    print(f"\nDone! Cek file: {audio_path}")
    print(f"Judul video: {script['title']}")
    print(f"Hashtags: {' '.join(script['hashtags'])}")