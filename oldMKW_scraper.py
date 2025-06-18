import os
from youtubesearchpython import VideosSearch
import yt_dlp
import subprocess

def get_video_urls(query, max_videos=20, max_allowed_minutes=60):
    videos_search = VideosSearch(query, limit=max_videos)
    results = videos_search.result()['result']
    filtered_urls = []

    for video in results:
        duration_str = video.get('duration')
        if duration_str:
            parts = list(map(int, duration_str.split(':')))
            if len(parts) == 3:  # HH:MM:SS
                total_minutes = parts[0] * 60 + parts[1]
            elif len(parts) == 2:  # MM:SS
                total_minutes = parts[0]
            else:
                continue

            if total_minutes <= max_allowed_minutes:
                filtered_urls.append(video['link'])

    return filtered_urls


def convert_to_compatible_mp4(input_path):
    base, _ = os.path.splitext(input_path)  
    output_path = base + '_clip.mp4' 

    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    duration_str = result.stdout.decode().strip()
    if not duration_str:
        print(f"Could not determine duration for {input_path}")
        return

    duration = float(duration_str)
    start_time = max(0, duration / 2 - 15)  

    cmd = f'ffmpeg -y -ss {start_time:.2f} -i "{input_path}" -t 30 -c:v libx264 -c:a aac -strict experimental -movflags +faststart "{output_path}"'
    print(f"Clipping 30s from middle: {input_path} -> {output_path}")
    os.system(cmd)

    if os.path.exists(output_path):
        os.remove(input_path)

    return output_path

def download_and_clip_video(url, output_path='./videos/'):
    os.makedirs(output_path, exist_ok=True)

    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info['title'].replace('/', '_')  
        filename = os.path.join(output_path, f"{title}.mp4")

    if os.path.exists(filename) or os.path.exists(filename.replace('.mp4', '_clip.mp4')):
        print(f"Already downloaded/clipped: {title}")
        return

    ydl_opts = {
        'outtmpl': filename,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'merge_output_format': 'mp4',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading {title} ...")
        ydl.download([url])

    convert_to_compatible_mp4(filename)

if __name__ == '__main__':
    query = 'Mario Kart World'
    max_videos = 50
    max_allowed_minutes = 60
    urls = get_video_urls(query, max_videos=max_videos, max_allowed_minutes=max_allowed_minutes)
    print(f"Found {len(urls)} videos under {max_allowed_minutes} minutes")
    for url in urls:
        download_and_clip_video(url)
