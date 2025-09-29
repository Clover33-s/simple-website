import json
import os
from src.scrapers.reddit_scraper import RedditScraper
from src.scrapers.tiktok_scraper import TikTokScraper
from src.video.compiler import VideoCompiler
from src.youtube.uploader import YouTubeUploader

def main():
    print("Starting Content Grinder...")

    with open('config.json') as f:
        config = json.load(f)

    media_urls = []

    # Scrape from Reddit if enabled
    if config.get('reddit', {}).get('enabled', False):
        print("Reddit scraping is enabled.")
        reddit_scraper = RedditScraper()
        media_urls.extend(reddit_scraper.get_media())

    # Scrape from TikTok if enabled
    if config.get('tiktok', {}).get('enabled', False):
        print("TikTok scraping is enabled.")
        tiktok_scraper = TikTokScraper()
        media_urls.extend(tiktok_scraper.get_media())

    if media_urls:
        print(f"Successfully fetched a total of {len(media_urls)} media items. Starting video compilation...")
        output_video_path = "final_video.mp4"
        compiler = VideoCompiler(media_urls)
        compiler.create_compilation(output_path=output_video_path)

        if os.path.exists(output_video_path):
            print("Video compiled successfully. Proceeding to upload...")
            uploader = YouTubeUploader()
            # Basic metadata - can be improved later
            video_title = "Awesome Content Compilation"
            video_description = "A compilation of the best content from the internet."
            video_tags = ["compilation", "memes", "funny", "reddit", "tiktok"]

            uploader.upload_video(output_video_path, video_title, video_description, video_tags)

            # Clean up the local video file after upload
            os.remove(output_video_path)
            print(f"Removed local video file: {output_video_path}")
        else:
            print("Video compilation failed. Cannot upload.")
    else:
        print("No media fetched from any source. Exiting.")

    print("Content Grinder finished.")

if __name__ == "__main__":
    main()