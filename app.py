from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from inference import generate_video
from utils import validate_faces
from watermark import add_watermark
import uuid, os, shutil
from concurrent.futures import ThreadPoolExecutor

# Set HuggingFace cache location to persistent workspace directory
os.environ["HF_HOME"] = "/workspace/models"
os.environ["TRANSFORMERS_CACHE"] = "/workspace/models"

# Initialize FastAPI app and thread pool
app = FastAPI()
executor = ThreadPoolExecutor(max_workers=1)

# Define directory paths
UPLOAD_DIR = "/workspace/uploads"
OUTPUT_DIR = "/workspace/output"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("/workspace/models", exist_ok=True)

# Job status tracker
STATUS = {}

# Plan configuration helper
def plan_config(plan):
    if plan == "free":
        return {"dur": 3, "watermark": True}
    return {"dur": 5, "watermark": False}

# Route: Generate video from 2 face images
@app.post("/generate")
async def generate(img1: UploadFile = File(...), img2: UploadFile = File(...), plan: str = Form(...)):
    job_id = str(uuid.uuid4())

    # Save uploaded images
    img1_path = os.path.join(UPLOAD_DIR, f"{job_id}_1.jpg")
    img2_path = os.path.join(UPLOAD_DIR, f"{job_id}_2.jpg")
    with open(img1_path, "wb") as f:
        f.write(await img1.read())
    with open(img2_path, "wb") as f:
        f.write(await img2.read())

    # Validate faces before submitting job
    if not validate_faces(img1_path, img2_path):
        os.remove(img1_path)
        os.remove(img2_path)
        raise HTTPException(status_code=400, detail="Invalid or undetectable faces in images.")

    STATUS[job_id] = "queued"
    config = plan_config(plan)

    # Run video generation in background
    executor.submit(process_job, job_id, img1_path, img2_path, config)

    return {"job_id": job_id}

# Background video generation function
def process_job(job_id, img1_path, img2_path, cfg):
    try:
        STATUS[job_id] = "processing"

        prompt = "Two heads, cinematic romantic lighting, k144ing kissing softly"
        video_path = generate_video(img1_path, img2_path, prompt, duration=cfg["dur"])

        # Add watermark if on free plan
        if cfg["watermark"]:
            watermarked_path = os.path.join(OUTPUT_DIR, f"{job_id}_wm.mp4")
            add_watermark(video_path, watermarked_path)
            final_path = watermarked_path
        else:
            final_path = os.path.join(OUTPUT_DIR, f"{job_id}.mp4")
            shutil.move(video_path, final_path)

        STATUS[job_id] = final_path

    except Exception as e:
        STATUS[job_id] = f"error: {str(e)}"

    finally:
        # Clean up input files
        for f in [img1_path, img2_path]:
            if os.path.exists(f):
                os.remove(f)

# Route: Check job status
@app.get("/status/{job_id}")
def status(job_id: str):
    state = STATUS.get(job_id, "not_found")
    if isinstance(state, str) and state.startswith("/workspace/output") and os.path.exists(state):
        return {"job_id": job_id, "status": "done", "video_url": state}
    elif isinstance(state, str) and state.startswith("error"):
        return {"job_id": job_id, "status": "error", "message": state}
    return {"job_id": job_id, "status": state}
