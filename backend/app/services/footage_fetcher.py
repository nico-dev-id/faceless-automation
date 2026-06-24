import os
import requests
from dotenv import load_dotenv

load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def search_videos(query: str, per_page: int = 5) -> list:
    """
    Cari video dari Pexels berdasarkan query.
    Returns list of video dict.
    """
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


def download_video(url: str, output_path: str, max_retries: int = 3) -> str:
    """
    Download video dari URL ke local path dengan retry.
    """
    headers = {"Authorization": PEXELS_API_KEY}
    
    for attempt in range(max_retries):
        try:
            print(f"Downloading (attempt {attempt + 1})...")
            response = requests.get(url, headers=headers, stream=True, timeout=30)
            
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Downloaded: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                print(f"Skipping {url} after {max_retries} attempts")
                return None
    
    return None


def get_footage_for_topic(topic: str, output_dir: str, max_videos: int = 3) -> list:
    """
    Search dan download video berdasarkan topik.
    Returns list of local video paths.
    """
    print(f"Searching footage for: {topic}")
    videos = search_videos(topic, per_page=max_videos)

    if not videos:
        print("No videos found, trying English query...")
        videos = search_videos("technology artificial intelligence", per_page=max_videos)

    downloaded = []
    for i, video in enumerate(videos[:max_videos]):
        output_path = os.path.join(output_dir, f"footage_{i+1}.mp4")
        download_video(video["url"], output_path)
        downloaded.append(output_path)

    return downloaded

def get_footage_per_segment(footage_keywords: list, output_dir: str) -> list:
    os.makedirs(output_dir, exist_ok=True)
    downloaded = []

    for i, segment in enumerate(footage_keywords):
        keyword = segment["keyword"]
        segment_name = segment["segment"]
        print(f"Searching footage for segment '{segment_name}': {keyword}")

        videos = search_videos(keyword, per_page=3)

        if not videos:
            print(f"No videos found for '{keyword}', trying fallback...")
            videos = search_videos("technology", per_page=3)

        for j, video in enumerate(videos[:3]):
            output_path = os.path.join(output_dir, f"segment_{i+1}_{segment_name}_{j+1}.mp4")
            result = download_video(video["url"], output_path)
            if result:
                downloaded.append(result)

    return downloaded