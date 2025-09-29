import os
import json
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from stability_sdk import client
from src.logger import log

class StabilityAIGenerator:
    def __init__(self, config_path='config.json'):
        """
        Initializes the Stability AI image generator.
        """
        with open(config_path) as f:
            config = json.load(f)

        ai_config = config.get('stability_ai', {})
        self.api_key = ai_config.get('api_key')
        self.output_dir = "temp_media"
        self.stability_api = None

        if self.api_key and "YOUR_STABILITY_AI_API_KEY" not in self.api_key:
            try:
                self.stability_api = client.StabilityInference(
                    key=self.api_key,
                    verbose=True,
                    engine="stable-diffusion-xl-1024-v1-0",
                )
                log.info("Stability AI client initialized successfully.")
            except Exception as e:
                log.error(f"Failed to initialize Stability AI client: {e}")
        else:
            log.warning("Stability AI API key not provided or is a placeholder. Generator will not run.")

    def generate_images(self, prompts):
        """
        Generates images from a given list of prompts and saves them.
        Returns a list of file paths to the generated images.
        """
        if not self.stability_api:
            log.error("Stability AI client not initialized. Cannot generate images.")
            return []

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            log.info(f"Created temporary media directory: {self.output_dir}")

        generated_image_paths = []
        log.info(f"Generating {len(prompts)} images using Stability AI...")

        for i, prompt_text in enumerate(prompts):
            try:
                log.info(f"Generating image for prompt: '{prompt_text}'")
                answers = self.stability_api.generate(prompt=prompt_text)

                for resp in answers:
                    for artifact in resp.artifacts:
                        if artifact.finish_reason == generation.FILTER:
                            log.warning(f"Could not generate image for prompt '{prompt_text}' due to safety filters.")
                        elif artifact.type == generation.ARTIFACT_IMAGE:
                            img_path = os.path.join(self.output_dir, f"gen_image_{i}.png")
                            with open(img_path, "wb") as f:
                                f.write(artifact.binary)
                            generated_image_paths.append(img_path)
                            log.info(f"Successfully saved generated image to {img_path}")
            except Exception as e:
                log.error(f"Failed to generate image for prompt '{prompt_text}'. Error: {e}")

        log.info(f"Finished generating images. Total images created: {len(generated_image_paths)}")
        return generated_image_paths

if __name__ == '__main__':
    # This is for testing the generator directly
    # Note: This will only work if you have a valid API key in config.json
    log.info("Testing StabilityAIGenerator directly...")
    generator = StabilityAIGenerator()
    # Define some example prompts for direct testing
    example_prompts = [
        "a majestic lion wearing a crown, studio portrait",
        "a robot painting a masterpiece, digital art"
    ]
    image_paths = generator.generate_images(prompts=example_prompts)
    if image_paths:
        log.info(f"Successfully generated {len(image_paths)} images.")
    else:
        log.warning("No images were generated. Check your API key in config.json.")