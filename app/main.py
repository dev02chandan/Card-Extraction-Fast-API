from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import google.generativeai as genai
from PIL import Image
import io
import os

# Configure the Google API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

app = FastAPI()

# EDIT THIS TO USE FOR YOUR USECASE (EXAMPLES GIVEN BELOW)
custom_prompt = 'Extract the number plate from the provided image of a truck. Return the result in a JSON format with the key "number_plate" and the value as the extracted number plate. If the number plate cannot be identified, return null for the value.'


# FOR EXTRACTING DRIVING LICENSE USE THIS:

custom_prompt2 = 'Extract the driving license number from the provided image of a driving license. Return the result in a JSON format with the key "driving_license_number" and the value as the extracted number. If the number cannot be identified, return null for the value.'

# FOR EXTRACTING CHASIS NUMBER USE THIS:

custom_prompt3 = 'Extract the chassis number from the provided image of a vehicle. Return the result in a JSON format with the key "chassis_number" and the value as the extracted number. If the number cannot be identified, return null for the value.'



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

