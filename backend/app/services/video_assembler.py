import os
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip

def create_subtitle_clips(words: list, total_duration: float, video_size: tuple) -> list:
    """
    Buat subtitle 3 kata sekaligus dengan timing proporsional.
    """
    subtitle_clips = []
    
    # Kelompokkan per 3 kata
    chunks = []
    for i in range(0, len(words), 3):
        chunk = " ".join(words[i:i+3])
        chunks.append(chunk)
    
    # Hitung total karakter untuk proporsi timing
    total_chars = sum(len(c) for c in chunks)
    
    current_time = 0.0
    
    for i, chunk in enumerate(chunks):
        # Durasi proporsional berdasarkan panjang chunk
        chunk_duration = (len(chunk) / total_chars) * total_duration
        
        txt_clip = TextClip(
            text=chunk,
            font_size=60,
            color="yellow",
            stroke_color="black",
            stroke_width=4,
            font="C:/Windows/Fonts/arialbd.ttf",
            method="caption",
            size=(900, 150),
        )
        
        txt_clip = txt_clip.with_start(current_time)
        txt_clip = txt_clip.with_duration(chunk_duration)
        txt_clip = txt_clip.with_position(("center", video_size[1] * 0.60))
        
        subtitle_clips.append(txt_clip)
        current_time += chunk_duration
    
    return subtitle_clips


def assemble_video(
    footage_paths: list,
    audio_path: str,
    output_path: str,
    script_text: str = "",
    target_duration: int = 60,
    clip_duration: int = 4
) -> str:
    """
    Gabungkan footage + audio + subtitle jadi video final.
    """
    print("Loading audio...")
    audio = AudioFileClip(audio_path)
    audio_duration = audio.duration
    print(f"Audio duration: {audio_duration:.2f} detik")

    print("Loading dan menyesuaikan footage...")
    clips = []
    total_duration = 0

    for path in footage_paths:
        if total_duration >= audio_duration:
            break

        clip = VideoFileClip(path)
        clip = clip.resized((1080, 1920))
        remaining = audio_duration - total_duration
        max_clip = min(clip_duration, clip.duration, remaining)
        clip = clip.subclipped(0, max_clip)
        clips.append(clip)
        total_duration += clip.duration
        print(f"Added: {os.path.basename(path)} ({clip.duration:.2f}s)")

    # Loop footage kalau kurang
    if total_duration < audio_duration:
        print("Footage kurang, looping dari awal...")
        i = 0
        while total_duration < audio_duration:
            path = footage_paths[i % len(footage_paths)]
            clip = VideoFileClip(path)
            clip = clip.resized((1080, 1920))
            remaining = audio_duration - total_duration
            max_clip = min(clip_duration, clip.duration, remaining)
            clip = clip.subclipped(0, max_clip)
            clips.append(clip)
            total_duration += clip.duration
            i += 1

    print(f"Total clips: {len(clips)}, Total duration: {total_duration:.2f}s")

    print("Menggabungkan footage...")
    final_video = concatenate_videoclips(clips)
    final_video = final_video.with_audio(audio)

    # Tambah subtitle kalau ada script
    if script_text:
        print("Membuat subtitle...")
        words = script_text.split()
        subtitle_clips = create_subtitle_clips(
            words=words,
            total_duration=audio_duration,
            video_size=(1080, 1920)
        )
        final_video = CompositeVideoClip([final_video] + subtitle_clips)

    print("Exporting video final...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final_video.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=30
    )

    audio.close()
    final_video.close()

    print(f"Video final saved: {output_path}")
    return output_path