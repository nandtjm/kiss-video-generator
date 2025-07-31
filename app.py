from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from inference import generate_video
from utils import validate_faces
from watermark import add_watermark
import uuid, os, shutil
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()
executor = ThreadPoolExecutor(max_workers=1)
UPLOAD="/workspace/uploads"; os.makedirs(UPLOAD, exist_ok=True)
RESULT="/workspace/output"; os.makedirs(RESULT, exist_ok=True)
STATUS={}

def plan_config(plan):
    if plan=="free": return {"dur":3,"watermark":True}
    return {"dur":5,"watermark":False}

@app.post("/generate")
async def generate(img1: UploadFile=File(...), img2: UploadFile=File(...), plan: str = Form(...)):
    job = str(uuid.uuid4())
    p1,p2 = os.path.join(UPLOAD,f"{job}_1.jpg"), os.path.join(UPLOAD,f"{job}_2.jpg")
    with open(p1,"wb") as f: shutil.copyfileobj(await img1.read(), f)
    with open(p2,"wb") as f: shutil.copyfileobj(await img2.read(), f)
    if not validate_faces(p1, p2):
        raise HTTPException(400, "Invalid faces")
    config = plan_config(plan)
    STATUS[job] = "queued"
    executor.submit(process_job, job, p1, p2, config)
    return {"job_id": job}

def process_job(job, p1, p2, cfg):
    STATUS[job] = "processing"
    prompt = "Two heads, cinematic romantic lighting, k144ing kissing softly"
    path = generate_video(p1, p2, prompt, duration=cfg["dur"])
    if cfg["watermark"]:
        wm = os.path.join(RESULT, f"{job}_wm.mp4")
        add_watermark(path, wm)
        path = wm
    final = os.path.join(RESULT, f"{job}.mp4")
    shutil.move(path, final)
    STATUS[job] = final

@app.get("/status/{job}")
def status(job:str):
    st = STATUS.get(job, "not_found")
    return {"job_id": job, "status": "done" if os.path.exists(STATUS.get(job,"")) else st,
            "video_url": STATUS[job] if os.path.exists(STATUS.get(job,"")) else None}
