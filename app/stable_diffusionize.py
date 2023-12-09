import base64
import io
from diffusers import StableDiffusionInpaintPipeline
from PIL import Image
import torch

# Load the model
pipe = StableDiffusionInpaintPipeline.from_pretrained(
    "runwayml/stable-diffusion-inpainting",
    variant="fp16",
    torch_dtype=torch.float32,
)

pipe.to("cuda")

def generate_image(input_image_path, prompt, color_hex):
    try:
        # Convert the prompt to a string
        if isinstance(prompt, dict):
            prompt = " ".join(prompt.values())

        # Open and resize the image to reduce resolution
        input_image = Image.open(io.BytesIO(input_image_path)).convert("RGB")
        input_image = input_image.resize((512, 512))

        # Generate a new image using the model
        image = pipe(
            prompt=prompt,
            image=input_image,
            mask_image=Image.new("RGB", (1, 1,), "white"),
            color_prompt=color_hex,
            num_inference_steps=5,
        ).images[0]

        # Save the generated image to the specified path
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        img_str = base64.b64encode(buffer.getvalue()).decode()

        return {"message": "Success", "output_image_path": img_str, "output_image": image}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"message": f"Error: {str(e)}", "output_image": None}
