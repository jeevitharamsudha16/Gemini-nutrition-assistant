### Health Management APP
from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-2.5-flash')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app

st.set_page_config(page_title="AI Nutrition Analyzer with Gemini Vision")

st.header("AI Nutrition Analyzer with Gemini Vision")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me the total calories")

input_prompt = """You are an expert nutritionist. Analyze the food items in the image and give the output in a clear, structured, and detailed format.

For each food item, provide the following fields in order:

- Item
- Calories (number only)
- Portion (describe size clearly)
- Macronutrients:
     Carbs_g
     Protein_g
     Fat_g
- Category (e.g., vegetable, grain, dairy, meat, seafood, fruit, snack)
- Health_Risk_Flags (if any)
- Interesting facts (1–2 detailed sentences about nutrition, benefits, or concerns)

After listing all items, provide:

- TOTAL_CALORIES (sum of all items, number only)
- Suggestion (2–3 detailed interesting sentences about overall meal quality)
- OVERALL_MODEL_CONFIDENCE (0–100)

Format your output EXACTLY like this:

1. <name>
   * Calories: <number>
   * Portion: <text>
   * Carbs_g: <number>
   * Protein_g: <number>
   * Fat_g: <number>
   * Category: <text>
   * Health_Risk_Flags: <text or none>
   * Interesting facts: <detailed text>

2. <name>
   * Calories: <number>
   * Portion: <text>
   * Carbs_g: <number>
   * Protein_g: <number>
   * Fat_g: <number>
   * Category: <text>
   * Health_Risk_Flags: <text or none>
   * Interesting facts: <detailed text>

TOTAL_CALORIES: <number>

Suggestion :<detailed text>

OVERALL_MODEL_CONFIDENCE: <0–100>
"""

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)
