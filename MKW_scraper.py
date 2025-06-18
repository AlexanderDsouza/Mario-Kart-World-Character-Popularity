import os
from youtubesearchpython import VideosSearch
import yt_dlp
import subprocess
import random


def get_many_video_urls(query, max_videos=2000, max_allowed_minutes=60):
    videos_search = VideosSearch(query, limit=20)
    all_videos = []
    seen_links = set()

    while len(all_videos) < max_videos:
        results = videos_search.result()['result']
        if not results:
            break

        for video in results:
            link = video.get('link')
            duration_str = video.get('duration')
            if not link or link in seen_links:
                continue

            parts = list(map(int, duration_str.split(':'))) if duration_str else []
            if len(parts) == 3:
                total_minutes = parts[0] * 60 + parts[1]
            elif len(parts) == 2:
                total_minutes = parts[0]
            else:
                continue

            if total_minutes <= max_allowed_minutes:
                all_videos.append(link)
                seen_links.add(link)

        # Paginate
        try:
            videos_search.next()
        except:
            break

    return all_videos[:max_videos]





def convert_to_compatible_mp4(input_path):
    base, _ = os.path.splitext(input_path)  
    output_path = base + '_clip.mp4' #making new filename _flip

    # Step 1: Get duration of video
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
    start_time = max(0, duration / 2 - 15)  # also catches 40s- ie 40/2 = 20 - 15= start at 5 seconds will still get 30 seconds

    # Step 2: Clip from the middle and re encode to make video viewable
    cmd = f'ffmpeg -y -ss {start_time:.2f} -i "{input_path}" -t 30 -c:v libx264 -c:a aac -strict experimental -movflags +faststart "{output_path}"'
    print(f"Clipping 30s from middle: {input_path} -> {output_path}")
    os.system(cmd)

    if os.path.exists(output_path):
        os.remove(input_path)

    return output_path




def download_and_clip_video(url, output_path='./videos/'):
    os.makedirs(output_path, exist_ok=True)

    # Step 1: Get video title

    ydl_opts = {
        'cookies': '/Users/alexd/Documents/MarioKartWorldCharacterCounter/cookies.txt',
        'format': 'best',
        'quiet': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info['title'].replace('/', '_')  # sanitize filename
        filename = os.path.join(output_path, f"{title}.mp4")

    if os.path.exists(filename) or os.path.exists(filename.replace('.mp4', '_converted.mp4')):
        print(f"Already downloaded: {title}")
        return
    

    # Step 2: Download raw video
    ydl_opts = {
        'outtmpl': filename,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'merge_output_format': 'mp4',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading {title} ...")
        ydl.download([url])

    # Step 3: Convert to QuickTime-compatible mp4
    convert_to_compatible_mp4(filename)


queries = [
    'Mario Kart World',
    'Mario Kart World gameplay',
    'Mario Kart highlights',
    'Mario Kart world tricks',
    'Mario Kart funny moments',
]


import os


for _ in range(10):  # 10 batches of 200 videos each = 2000 total
    query = random.choice(queries)
    print(f"Batch query: {query}")
    urls = get_many_video_urls(query, max_videos=200, max_allowed_minutes=60)
    for url in urls:
        download_and_clip_video(url)
