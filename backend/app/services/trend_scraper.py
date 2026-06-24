import os
import feedparser
from pytrends.request import TrendReq
from dotenv import load_dotenv

load_dotenv()

def get_google_trends(niche: str = "teknologi", region: str = "ID") -> list:
    """
    Ambil trending topics dari Google Trends untuk Indonesia.
    """
    try:
        pytrends = TrendReq(hl='id-ID', tz=420)  # tz=420 untuk WIB
        
        # Mapping niche ke keyword seed
        niche_keywords = {
            "teknologi": ["teknologi", "aplikasi", "smartphone", "AI", "internet"],
            "bisnis": ["bisnis", "investasi", "saham", "startup", "entrepreneur"],
            "kesehatan": ["kesehatan", "diet", "olahraga", "vitamin", "dokter"],
            "hiburan": ["film", "musik", "drama", "artis", "konser"],
            "pendidikan": ["belajar", "kuliah", "beasiswa", "kursus", "skill"],
        }
        
        keywords = niche_keywords.get(niche, ["teknologi"])
        
        # Ambil related queries yang trending
        pytrends.build_payload(keywords[:3], cat=0, timeframe='now 1-d', geo=region)
        related = pytrends.related_queries()
        
        topics = []
        for keyword in keywords[:3]:
            if keyword in related and related[keyword]['top'] is not None:
                df = related[keyword]['top']
                for _, row in df.head(3).iterrows():
                    topics.append({
                        "topic": row['query'],
                        "value": int(row['value']),
                        "source": "google_trends",
                        "niche": niche
                    })
        
        # Sort by value (popularity)
        topics = sorted(topics, key=lambda x: x['value'], reverse=True)
        return topics[:10]
    
    except Exception as e:
        print(f"Google Trends error: {e}")
        return []


def get_rss_trends(niche: str = "teknologi") -> list:
    """
    Ambil trending topics dari RSS Feed berita Indonesia sebagai backup.
    """
    rss_feeds = {
        "teknologi": [
            "https://www.cnnindonesia.com/teknologi/rss",
            "https://tekno.kompas.com/feed/",
        ],
        "bisnis": [
            "https://www.cnnindonesia.com/ekonomi/rss",
            "https://ekonomi.kompas.com/feed/",
        ],
        "kesehatan": [
            "https://www.cnnindonesia.com/gaya-hidup/rss",
            "https://health.kompas.com/feed/",
        ],
        "hiburan": [
            "https://www.cnnindonesia.com/hiburan/rss",
            "https://entertainment.kompas.com/feed/",
        ],
        "pendidikan": [
            "https://www.cnnindonesia.com/nasional/rss",
            "https://edukasi.kompas.com/feed/",
        ],
    }

    feeds = rss_feeds.get(niche, rss_feeds["teknologi"])
    topics = []

    for feed_url in feeds:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:5]:
                topics.append({
                    "topic": entry.title,
                    "value": 100,
                    "source": "rss",
                    "niche": niche
                })
        except Exception as e:
            print(f"RSS error {feed_url}: {e}")

    return topics[:10]


def get_trending_topics(niche: str = "teknologi") -> list:
    """
    Gabungkan Google Trends + RSS Feed.
    Google Trends sebagai primary, RSS sebagai fallback.
    """
    print(f"Fetching trending topics untuk niche: {niche}")
    
    topics = get_google_trends(niche)
    
    if len(topics) < 3:
        print("Google Trends kurang, tambah dari RSS...")
        rss_topics = get_rss_trends(niche)
        topics.extend(rss_topics)
    
    print(f"Total topics ditemukan: {len(topics)}")
    return topics


if __name__ == "__main__":
    topics = get_trending_topics("teknologi")
    print("\nTRENDING TOPICS:")
    for i, t in enumerate(topics, 1):
        print(f"{i}. [{t['source']}] {t['topic']} (value: {t['value']})")