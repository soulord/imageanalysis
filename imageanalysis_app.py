import base64
from PIL import Image as PILImage
from langchain_openai import OpenAI
import streamlit as st


api_key = "sk-proj-ReIwb6sECBqdpCkiqSq8T3BlbkFJYzLbXtecaS12V7yMpJLX"

OpenAI.api_key = api_key


# Function to encode image to base64
def encode_image64(uploaded_file):
    return base64.b64encode(uploaded_file.read()).decode("utf-8")

# Function to analyze the image description
def analyze_image(prompt, base64_image):
    response = OpenAI.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {"role": "system", "content": "You are an assisstant."},
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                }
            ]}
      ]
    )

    return response.choices[0].message.content

st.title("Image Analysis with OpenAI")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    img = PILImage.open(uploaded_file)
    st.image(img, caption='Uploaded Image', use_column_width=True)

    # Encode the uploaded image to base64
    uploaded_file.seek(0)  
    base64_image = encode_image64(uploaded_file)

    # Get user input for the prompt
    user_prompt = st.text_input("Enter a description of the image and your question:")

    if st.button("Analyze"):
        try:
            response_content = analyze_image(user_prompt, base64_image)
            st.write(response_content)
        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    st.write("Please upload an image to analyze.")
