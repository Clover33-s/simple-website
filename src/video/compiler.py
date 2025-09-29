from moviepy.editor import ImageClip, VideoFileClip, concatenate_videoclips
import os
from src.logger import log

class VideoCompiler:
    def __init__(self, media_paths):
        """
        Initializes the VideoCompiler with a list of local media file paths.
        """
        self.media_paths = media_paths
        self.temp_dir = "temp_media"

    def create_compilation(self, output_path="final_video.mp4", image_duration=5):
        """
        Creates a video compilation from the provided media paths.
        """
        if not self.media_paths:
            log.error("No media paths provided. Cannot create video.")
            return

        clips = []
        log.info("Creating video clips from media files...")
        for path in self.media_paths:
            try:
                if path.lower().endswith(('.jpg', '.jpeg', '.png')):
                    clip = ImageClip(path, duration=image_duration)
                elif path.lower().endswith('.gif'):
                    clip = VideoFileClip(path)
                elif path.lower().endswith('.mp4'):
                    clip = VideoFileClip(path)
                else:
                    log.warning(f"Skipping unsupported file format: {path}")
                    continue

                # Standardize clip size
                clip = clip.resize(width=1024, height=1024) # Adjusted for common AI image sizes
                clips.append(clip)
            except Exception as e:
                log.error(f"Failed to process file {path}. Error: {e}")

        if not clips:
            log.error("No valid clips to compile.")
            return

        log.info(f"Concatenating {len(clips)} clips into a final video...")
        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24, logger='bar')

        # Clean up temporary files
        for clip in clips:
            clip.close()
        self.cleanup()

        log.info(f"Video compilation successful! Saved to {output_path}")

    def cleanup(self):
        log.info(f"Cleaning up temporary files in {self.temp_dir}...")
        try:
            # Only clean up if the directory exists
            if os.path.exists(self.temp_dir):
                for file_name in os.listdir(self.temp_dir):
                    os.remove(os.path.join(self.temp_dir, file_name))
                os.rmdir(self.temp_dir)
                log.info("Cleanup successful.")
        except OSError as e:
            log.error(f"Error during cleanup: {e}")