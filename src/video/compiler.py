import requests
from moviepy.editor import ImageClip, VideoFileClip, concatenate_videoclips
import os

class VideoCompiler:
    def __init__(self, media_urls):
        self.media_urls = media_urls
        self.temp_dir = "temp_media"
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def download_media(self):
        local_paths = []
        for i, url in enumerate(self.media_urls):
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()

                # Guess the file extension
                file_ext = url.split('.')[-1].split('?')[0]
                if file_ext not in ['jpg', 'jpeg', 'png', 'mp4', 'gif']:
                    # A basic fallback
                    content_type = response.headers.get('Content-Type')
                    if 'image' in content_type:
                        file_ext = 'jpg'
                    elif 'video' in content_type:
                        file_ext = 'mp4'
                    else:
                        print(f"Skipping unsupported content type for URL: {url}")
                        continue

                file_path = os.path.join(self.temp_dir, f"media_{i}.{file_ext}")

                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                local_paths.append(file_path)
            except requests.exceptions.RequestException as e:
                print(f"Failed to download {url}. Error: {e}")
        return local_paths

    def create_compilation(self, output_path="final_video.mp4", image_duration=5):
        local_media_paths = self.download_media()
        if not local_media_paths:
            print("No media downloaded. Cannot create video.")
            return

        clips = []
        for path in local_media_paths:
            try:
                if path.lower().endswith(('.jpg', '.jpeg', '.png')):
                    clip = ImageClip(path, duration=image_duration)
                elif path.lower().endswith('.gif'):
                    clip = VideoFileClip(path)
                elif path.lower().endswith('.mp4'):
                    clip = VideoFileClip(path)
                else:
                    print(f"Skipping unsupported file format: {path}")
                    continue

                # Standardize clip size
                clip = clip.resize(width=1920, height=1080)
                clips.append(clip)
            except Exception as e:
                print(f"Failed to process file {path}. Error: {e}")

        if not clips:
            print("No valid clips to compile.")
            return

        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24)

        # Clean up temporary files
        for clip in clips:
            clip.close()
        self.cleanup()

        print(f"Video compilation successful! Saved to {output_path}")

    def cleanup(self):
        for file_name in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file_name))
        os.rmdir(self.temp_dir)