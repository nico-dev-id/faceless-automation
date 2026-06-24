import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_script(topic: str, niche: str = "teknologi") -> dict:
    """
    Generate script video 60 detik dari topik yang diberikan.
    Returns dict dengan intro, content, outro, dan full_script.
    """
    
    prompt = f"""Kamu adalah script writer profesional untuk YouTube Shorts Indonesia.
    
Buat script video YouTube Shorts berdurasi 60 detik tentang: "{topic}"
Niche: {niche}
Bahasa: Indonesia (casual, engaging, mudah dipahami)

Script harus terdiri dari:
1. INTRO (10 detik): HOOK yang membuat orang BERHENTI SCROLL. 
   Gunakan salah satu teknik ini:
   - Fakta mengejutkan: "90% orang tidak tahu bahwa..."
   - Pertanyaan provokatif: "Kamu mau digantikan robot tahun depan?"
   - Pernyataan kontroversial: "Kuliah 4 tahun akan sia-sia karena ini..."
   - Angka spesifik: "5 pekerjaan ini akan hilang dalam 2 tahun!"
   Hook HARUS di kalimat PERTAMA, langsung to the point, tanpa basa-basi.

2. ISI (40 detik): Informasi yang MENGEJUTKAN dan SPESIFIK.
   - Gunakan contoh nyata dan angka spesifik
   - Gunakan konteks Indonesia (perusahaan lokal, situasi lokal)
   - Setiap poin harus membuat penonton berpikir "oh ternyata!"
   - Bangun rasa urgensi — penonton harus merasa ini penting SEKARANG

3. OUTRO (10 detik): Call to action (like, subscribe, komen)

PENTING:
- Gunakan bahasa Indonesia yang natural dan tidak kaku
- Total kata sekitar 150-180 kata (sesuai 60 detik berbicara)
- Untuk footage_keywords, gunakan deskripsi VISUAL yang bisa ditemukan di stock footage
- Keyword harus menggambarkan ADEGAN NYATA yang terlihat di kamera, bukan konsep abstrak
- Contoh BURUK: "artificial intelligence", "technology future"
- Contoh BAGUS: "person using laptop cafe", "robot hand moving factory", "businessman stressed office"

Respond HANYA dengan JSON format ini, tanpa preamble apapun:
{{
    "intro": "teks intro disini",
    "content": "teks isi disini",
    "outro": "teks outro disini",
    "full_script": "intro + content + outro digabung",
    "title": "judul video yang menarik",
    "hashtags": ["hashtag1", "hashtag2", "hashtag3", "hashtag4", "hashtag5"],
    "footage_keywords": [
        {{"segment": "intro", "keyword": "deskripsi visual adegan nyata dalam bahasa inggris, contoh: person shocked looking at phone screen"}},
        {{"segment": "content_1", "keyword": "deskripsi visual adegan nyata dalam bahasa inggris, contoh: robot arm working in factory"}},
        {{"segment": "content_2", "keyword": "deskripsi visual adegan nyata dalam bahasa inggris"}},
        {{"segment": "content_3", "keyword": "deskripsi visual adegan nyata dalam bahasa inggris"}},
        {{"segment": "outro", "keyword": "deskripsi visual adegan nyata dalam bahasa inggris, contoh: person giving thumbs up smiling"}}
    ]
}}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000
    )
    
    raw = response.choices[0].message.content.strip()
    
    # Bersihkan jika ada markdown code block
    raw = raw.replace("```json", "").replace("```", "").strip()
    
    result = json.loads(raw)
    return result


if __name__ == "__main__":
    print("Testing script generator...")
    script = generate_script(
        topic="Cara AI mengubah dunia kerja di tahun 2025",
        niche="teknologi"
    )
    print(f"\nJUDUL: {script['title']}")
    print(f"\nINTRO:\n{script['intro']}")
    print(f"\nISI:\n{script['content']}")
    print(f"\nOUTRO:\n{script['outro']}")
    print(f"\nHASHTAGS: {' '.join(script['hashtags'])}")
    print(f"\nTotal karakter: {len(script['full_script'])}")