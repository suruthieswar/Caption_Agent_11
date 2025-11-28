import uvicorn
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from fastapi.responses import FileResponse
import os
import tempfile
import time

app = FastAPI()

@app.get("/")
def read_index():
    index_file = ROOT / "index.html"
    return FileResponse(index_file)
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini
GOOGLE_API_KEY = "AIzaSyCA9y-RC2g6tEnATjA5iHQuF-vHjzqrsQs"
genai.configure(api_key=GOOGLE_API_KEY)

@app.post("/generate")
async def generate_caption(file: UploadFile = File(...), style: str = Form(...)):
    # Save uploaded file temporarily
    suffix = ".mp4" if "video" in file.content_type else ".jpg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        # Upload to Gemini
        mime = "video/mp4" if "video" in file.content_type else "image/jpeg"
        ai_file = genai.upload_file(tmp_path, mime_type=mime)
        
        # Wait for processing if video
        while ai_file.state.name == "PROCESSING":
            time.sleep(2)
            ai_file = genai.get_file(ai_file.name)

        # Generate Caption
        model = genai.GenerativeModel('gemini-flash-latest')
        
        style_prompts = {
            "viral": "Write a viral caption that sounds like a real person. Short, punchy, and trending. Max 2 lines. No robotic enthusiasm. Make it more really one",
            "story": "Tell a mini-story about this. Emotional and descriptive, like a personal blog post. Avoid generic AI phrases.Make it more really one",
            "witty": "Write a witty and fun caption. Clever, maybe a bit sassy, but natural. Like a friend making a joke.Make it more really one",
            "engagement": "Write a caption that naturally sparks conversation. Ask a genuine question or encourage comments without sounding desperate.Make it more really one"
        }
        
        selected_prompt = style_prompts.get(style, style_prompts["viral"])
        
        prompt = (
            f"Analyze this image/video. {selected_prompt} "
            "Write like a human on social media, not an AI. Use natural language, lower case if it fits the vibe. "
            "Include relevant emojis and 3-5 hashtags. "
            "Output ONLY the caption text."
        )
        
        response = model.generate_content([prompt, ai_file])
        return {"caption": response.text}
    except Exception as e:
        return {"caption": f"Error: {str(e)}"}
    finally:
        # Cleanup
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

ROOT = Path(__file__).resolve().parent