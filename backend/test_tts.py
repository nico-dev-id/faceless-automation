from gtts import gTTS
import os

def generate_audio(text: str, output_path: str, lang: str = "id"):
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(output_path)
    print(f"Audio saved: {output_path}")

sample_text = """
Halo semuanya! Selamat datang di channel ini.
Hari ini kita akan membahas tentang kecerdasan buatan 
dan bagaimana teknologi ini mengubah dunia kita.
Tetap tonton sampai habis ya!
"""

if __name__ == "__main__":
    os.makedirs("test_output", exist_ok=True)
    generate_audio(sample_text, "test_output/sample_audio.mp3")
    print("Buka file test_output/sample_audio.mp3 untuk dengarkan hasilnya!")