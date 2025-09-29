import praw
import json

class RedditScraper:
    def __init__(self, config_path='config.json'):
        with open(config_path) as f:
            config = json.load(f)

        reddit_config = config.get('reddit', {})
        self.subreddits = reddit_config.get('subreddits', [])
        self.limit = reddit_config.get('limit', 10)
        self.timeframe = reddit_config.get('timeframe', 'day')

        try:
            # PRAW will automatically look for a praw.ini file in the current directory
            # and use the "bot1" section to configure the instance.
            # The user_agent should be set in that file.
            self.reddit = praw.Reddit("bot1")
        except Exception as e:
            print(f"Could not initialize PRAW. Please check your praw.ini or environment variables. Error: {e}")
            self.reddit = None

    def get_media(self):
        if not self.reddit:
            print("PRAW not initialized. Cannot fetch media.")
            return []

        media_urls = []
        for subreddit_name in self.subreddits:
            print(f"Scraping subreddit: r/{subreddit_name}")
            subreddit = self.reddit.subreddit(subreddit_name)
            try:
                hot_posts = subreddit.top(time_filter=self.timeframe, limit=self.limit)
                for post in hot_posts:
                    if not post.is_self:
                        # Handle images and gifs
                        if post.url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                            media_urls.append(post.url)
                        # Handle v.redd.it videos
                        elif post.is_video:
                            if post.media and 'reddit_video' in post.media:
                                # This URL is typically video-only. Split to remove query params.
                                media_urls.append(post.media['reddit_video']['fallback_url'].split('?')[0])
            except Exception as e:
                print(f"Could not scrape subreddit {subreddit_name}. Error: {e}")

        return media_urls

if __name__ == '__main__':
    # This is for testing the scraper directly
    scraper = RedditScraper()
    media = scraper.get_media()
    if media:
        print(f"Found {len(media)} media items.")
        for url in media:
            print(url)
    else:
        print("No media found or PRAW not configured.")