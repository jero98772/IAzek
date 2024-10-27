import webuiapi
import random
from typing import Optional

class ImageGenerator:
    def __init__(self, host: str, port: int):
        self.api = webuiapi.WebUIApi(host=host, port=port)

    def generate_image(self, prompt: str) -> str:
        result = self.api.txt2img(
            prompt=prompt,
            negative_prompt="(deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4), disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation",
            seed=random.randint(0, 10000),
            steps=25,
            sampler_index='DDIM',
            enable_hr=True,
            hr_scale=2,
            hr_upscaler=webuiapi.HiResUpscaler.Latent,
            hr_second_pass_steps=20,
            hr_resize_x=524,
            hr_resize_y=524,
            denoising_strength=0.4,
            cfg_scale=7,
        )
        image_path = 'generated_image.png'
        result.image.save(image_path)
        return image_path