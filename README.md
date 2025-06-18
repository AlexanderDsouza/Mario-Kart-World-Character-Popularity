# 🏎️ Mario Kart World Character Popularity Tracker

This project aims to identify the most popular characters being played in **Mario Kart World** by combining web scraping and computer vision.

## 🧠 Project Overview

The goal is to:

1. **Scrape gameplay footage** from YouTube or other platforms like Twitch.
2. **Extract frames** or short clips from those videos.
3. **Apply computer vision techniques** (e.g. convolutional neural networks) to identify which character is being played in each clip.
4. **Aggregate and visualize** the data to determine the most popular characters being used in real-world gameplay.

## 📦 Current Status

- Implemented a YouTube video scraper using `yt-dlp`.
- Investigating workarounds for bot detection and authentication issues (e.g. cookies).
- Planning to apply a CNN-based classifier to identify characters in gameplay frames.
- Final goal: Display character usage statistics based on real gameplay data.

## ⚠️ Important Notes

- Due to YouTube’s bot detection, this project may require a `cookies.txt` file for authenticated scraping.  
- Refer to the [yt-dlp FAQ](https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp) for instructions on exporting cookies from your browser.
