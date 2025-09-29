import os
import json
from openai import OpenAI
from src.logger import log

class IdeaGenerator:
    def __init__(self, config_path='config.json'):
        """
        Initializes the Idea Generator with settings from the config file.
        """
        with open(config_path) as f:
            config = json.load(f)

        llm_config = config.get('llm_generator', {})
        self.api_key = llm_config.get('api_key')
        self.model = llm_config.get('model', 'gpt-4o-mini')
        self.theme = llm_config.get('theme', 'A series of random, interesting images.')
        self.prompt_count = llm_config.get('prompt_count', 5)
        self.client = None

        if self.api_key and "YOUR_OPENAI_API_KEY" not in self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
                log.info("OpenAI client initialized successfully.")
            except Exception as e:
                log.error(f"Failed to initialize OpenAI client: {e}")
        else:
            log.warning("OpenAI API key not provided or is a placeholder. Idea generator will not run.")

    def generate_prompts(self):
        """
        Connects to the LLM to generate a list of image prompts based on a theme.
        """
        if not self.client:
            log.error("OpenAI client not initialized. Cannot generate prompts.")
            return []

        log.info(f"Generating {self.prompt_count} image prompts based on the theme: '{self.theme}'")

        system_prompt = (
            "You are an expert creative director. Your task is to generate a numbered list of "
            f"{self.prompt_count} distinct, highly detailed, and visually compelling image prompts suitable for an AI image generator like Stable Diffusion. "
            "Each prompt should be a single, descriptive sentence. The prompts should all be based on the following theme: "
            f"'{self.theme}'. Do not include any extra text, just the numbered list of prompts."
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Please generate the {self.prompt_count} prompts."}
                ],
                temperature=0.8,
            )

            content = response.choices[0].message.content
            # Parse the numbered list from the response
            prompts = [line.split('. ', 1)[1] for line in content.strip().split('\n') if '. ' in line]

            if prompts:
                log.info("Successfully generated the following prompts:")
                for p in prompts:
                    log.info(f"  - {p}")
                return prompts
            else:
                log.error("Failed to parse prompts from the LLM response.")
                return []

        except Exception as e:
            log.error(f"An error occurred while generating prompts from the LLM: {e}")
            return []

if __name__ == '__main__':
    # This is for testing the generator directly
    log.info("Testing IdeaGenerator directly...")
    idea_gen = IdeaGenerator()
    generated_prompts = idea_gen.generate_prompts()
    if generated_prompts:
        log.info(f"Successfully generated {len(generated_prompts)} prompts.")
    else:
        log.warning("No prompts were generated. Check your API key and theme in config.json.")