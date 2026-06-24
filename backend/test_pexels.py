import requests
import os
from dotenv import load_dotenv

load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def search_videos(query: str, per_page: int = 3):
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": query,
        "per_page": per_page,
        "orientation": "portrait",
        "size": "medium"
    }
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    videos = []
    for video in data.get("videos", []):
        video_files = video.get("video_files", [])
        hd_file = next(
            (f for f in video_files if f.get("quality") == "hd"),
            video_files[0] if video_files else None
        )
        if hd_file:
            videos.append({
                "id": video["id"],
                "url": hd_file["link"],
                "duration": video["duration"],
                "width": hd_file["width"],
                "height": hd_file["height"]
            })
    
    return videos

if __name__ == "__main__":
    results = search_videos("teknologi artificial intelligence")
    for v in results:
        print(f"ID: {v['id']}")
        print(f"URL: {v['url']}")
        print(f"Duration: {v['duration']}s")
        print(f"Resolution: {v['width']}x{v['height']}")
        print("---")