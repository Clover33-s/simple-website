import json
import os
from src.logger import log
from src.scrapers.reddit_scraper import RedditScraper
from src.scrapers.tiktok_scraper import TikTokScraper
from src.video.compiler import VideoCompiler
from src.youtube.uploader import YouTubeUploader

def main():
    log.info("Starting Content Grinder...")

    try:
        with open('config.json') as f:
            config = json.load(f)
    except FileNotFoundError:
        log.error("Configuration file 'config.json' not found. Please ensure it exists.")
        return

    media_urls = []

    # Scrape from Reddit if enabled
    if config.get('reddit', {}).get('enabled', False):
        log.info("Reddit scraping is enabled.")
        reddit_scraper = RedditScraper()
        media_urls.extend(reddit_scraper.get_media())

    # Scrape from TikTok if enabled
    if config.get('tiktok', {}).get('enabled', False):
        log.info("TikTok scraping is enabled.")
        tiktok_scraper = TikTokScraper()
        media_urls.extend(tiktok_scraper.get_media())

    if media_urls:
        log.info(f"Successfully fetched a total of {len(media_urls)} media items. Starting video compilation...")
        output_video_path = "final_video.mp4"
        compiler = VideoCompiler(media_urls)
        compiler.create_compilation(output_path=output_video_path)

        if os.path.exists(output_video_path):
            log.info("Video compiled successfully. Proceeding to upload...")
            uploader = YouTubeUploader()
            # Basic metadata - can be improved later
            video_title = "Awesome Content Compilation"
            video_description = "A compilation of the best content from the internet."
            video_tags = ["compilation", "memes", "funny", "reddit", "tiktok"]

            uploader.upload_video(output_video_path, video_title, video_description, video_tags)

            # Clean up the local video file after upload
            try:
                os.remove(output_video_path)
                log.info(f"Removed local video file: {output_video_path}")
            except OSError as e:
                log.error(f"Error removing local video file: {e}")
        else:
            log.error("Video compilation failed. Cannot upload.")
    else:
        log.warning("No media fetched from any source. Exiting.")

    log.info("Content Grinder finished.")

if __name__ == "__main__":
    main()