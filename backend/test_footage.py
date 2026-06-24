import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.footage_fetcher import get_footage_for_topic

if __name__ == "__main__":
    print("Testing footage fetcher...")
    
    videos = get_footage_for_topic(
        topic="artificial intelligence technology",
        output_dir="test_output/footage",
        max_videos=3
    )
    
    print(f"\nDone! {len(videos)} video downloaded:")
    for v in videos:
        print(f"  - {v}")