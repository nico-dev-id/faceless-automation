import os
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()

def generate_audio(text: str, output_path: str, lang: str = "id") -> str:
    """
    Generate audio dari teks script.
    Returns path file audio yang dihasilkan.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(output_path)
    
    print(f"Audio generated: {output_path}")
    return output_path