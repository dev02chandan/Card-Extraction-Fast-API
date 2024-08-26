from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import google.generativeai as genai
from PIL import Image
import io
import os

# Configure the Google API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

app = FastAPI()

# Define the prompt
custom_prompt = "Extract Name, designation, mobile number, Email Id, and City in JSON proper spelling"

@app.post("/extract-info/")
async def extract_info(file: UploadFile = File(...)):
    try:
        # Ensure the uploaded file is an image
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload a jpg, jpeg, or png image.")
        
        # Read the image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Load and process the image with Gemini AI
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
        response = model.generate_content([custom_prompt, image])
        f = open("app/test.txt", 'a')
        f.write(response.text)
        f.close()
        # Return the response text as JSON
        return JSONResponse(content={"text": response.text})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

