from moviepy import VideoFileClip
import requests
import os
from dotenv import load_dotenv

load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def download_video(url: str, output_path: str):
    print(f"Downloading video...")
    headers = {"Authorization": PEXELS_API_KEY}
    response = requests.get(url, headers=headers, stream=True)
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded: {output_path}")

def test_clip_video(input_path: str, output_path: str, duration: int = 5):
    clip = VideoFileClip(input_path)
    short_clip = clip.subclipped(0, min(duration, clip.duration))
    short_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    clip.close()
    print(f"Video saved: {output_path}")

if __name__ == "__main__":
    os.makedirs("test_output", exist_ok=True)
    
    video_url = "https://videos.pexels.com/video-files/8087078/8087078-hd_1080_1920_25fps.mp4"
    
    download_video(video_url, "test_output/sample_video.mp4")
    test_clip_video("test_output/sample_video.mp4", "test_output/clipped_video.mp4", duration=5)
    print("Done! Cek file test_output/clipped_video.mp4")