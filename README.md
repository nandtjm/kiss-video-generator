# AI Kiss Video Generator

This project allows users to generate a kissing video using two uploaded human images. It offers a free plan with limited resolution and duration, and a paid plan with enhanced quality and longer videos.

## Features

* ✅ Input: Two clear human face images
* ✅ Validation: Check both images are real humans before processing
* ✅ Output: Video (3s to 8s), with watermark for free plan users
* ✅ Free: 480p 3s kissing video, with watermark
* ✅ Paid: 720p or 1080p video, 5-8s, no watermark
* ✅ Backend: RunPod REST API using actual model
* ✅ Progress status updates during processing
* ✅ Video upscaling available (paid users)

---

## Deployment Options

### 🟢 RunPod (Recommended for Production)

#### Setup Instructions

1. Clone this repo:

```bash
git clone https://github.com/your-username/ai-kiss-video-generator.git
cd ai-kiss-video-generator
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set environment variables:

```bash
export RUNPOD_API_KEY=your_runpod_key
export MODEL_ID=wan-derful/wan2.2-ti2v-5b  # or wan2.1-t2v-14b for high quality
```

4. Start FastAPI server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## API Docs

### `POST /generate`

**Description**: Generate a kissing video using two human face images.

**Request Body (multipart/form-data)**:

```json
{
  "image1": File (image),
  "image2": File (image),
  "plan": "free" | "paid"
}
```

**Response**:

```json
{
  "status": "processing",
  "video_url": "https://...",
  "estimated_time": "90 seconds"
}
```

### `GET /status/{task_id}`

**Description**: Get progress of a currently processing video.

---

## Models Used

| Model                       | Description          | RunPod Cost | Suitable For     |
| --------------------------- | -------------------- | ----------- | ---------------- |
| `wan-derful/wan2.2-ti2v-5b` | Lightweight, faster  | \~\$0.06/hr | RunPod & testing |
| `wan-derful/wan2.1-t2v-14b` | High-quality, slower | \~\$0.10/hr | Paid production  |

---

## Notes

* Free plan videos have watermarks and shorter duration.
* Paid plan removes watermark and allows 720p/1080p export.
* Video processing time: \~60-90 seconds.
* Upscaling available via separate endpoint.

---

## License

MIT License
