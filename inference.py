import torch, imageio, os
from diffusers import WanImageToVideoPipeline
from utils import merge_side_by_side

# 🧠 Set cache directory to persistent path
os.environ["HF_HOME"] = "/workspace/models"
os.environ["TRANSFORMERS_CACHE"] = "/workspace/models"

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 🧠 Load model with cache directory
pipe = WanImageToVideoPipeline.from_pretrained(
    "Wan-AI/Wan2.2-TI2V-5B-Diffusers",
    torch_dtype=torch.float16,
    cache_dir="/workspace/models",
    low_cpu_mem_usage=False,
    ignore_mismatched_sizes=True
)

pipe = pipe.to(DEVICE)
pipe.enable_attention_slicing()
pipe.load_lora_weights("Remade-AI/kissing", bias="none", use_safetensors=True)

def generate_video(img1, img2, prompt, duration=5):
    merged = merge_side_by_side(img1, img2)

    out = pipe(
        image=merged,
        prompt=prompt,
        num_frames=duration * 24,
        height=512,
        width=1024,
        guidance_scale=6.0,
        lr_frame_flow_shift=5.0
    )

    video = out.frames

    # Save output video in a persistent path
    path = f"/workspace/output/output_{torch.randint(0,9999,(1,)).item()}.mp4"
    imageio.mimwrite(path, video, fps=24, codec='libx264', quality=8)

    return path
