import base64
import google.generativeai as genai
from io import BytesIO
from pdf2image import convert_from_path
from PIL import Image
import os
import requests

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")

api_key = os.getenv("GEMINI_API_KEY", "")
genai.configure(api_key=api_key)


credentials = f"{ACCOUNT_SID}:{AUTH_TOKEN}"
encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
headers = {"Authorization": f"Basic {encoded_credentials}"}

class ImageInterpreter():
    def __init__(self, api_key=api_key, model="gemini-pro-vision"):
        self.api_key = api_key
        self.model = genai.GenerativeModel(model_name=model)

    @classmethod
    def load_image_from_url(cls, url):
        try:       
            response = requests.get(url, headers=headers, stream=True)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                return image
            else:
                print('Error loading the image. Error code:', response.status_code)
                return None
        except Exception as e:
            print('Error loading the image:', e)
            return None

    @classmethod
    def load_image_from_path(cls, path):
        try:
            image = Image.open(path)
            return image
        except Exception as e:
            print('Error loading the image:', e)
            return None

    @classmethod
    def load_image(cls, image_path):
        if image_path.startswith("http"):
            img = cls.load_image_from_url(image_path)
        else:
            img = cls.load_image_from_path(image_path)
        return img

    @classmethod
    def show_image(cls, image_path, size_prop=0.5):        
        img = cls.load_image(image_path)
        width = int(img.width * size_prop)
        height = int(img.height * size_prop)
        return img.resize((width, height))

    def query_image(self, image, query):
        # verify if image is an string
        if isinstance(image, str):
            image_path = image
            img = self.load_image(image_path)
        else:
            img = image
        response = self.model.generate_content([query, img])
        return response.text

class PDFInterpreter():
    def __init__(self, api_key=api_key, model="gemini-pro-vision"):
        self.vi = ImageInterpreter(api_key=api_key, model=model)

    
    @classmethod
    def save_pdf_in_tmp(self, pdf_url):
        response = requests.get(pdf_url)
        if response.status_code == 200:
            with open('/tmp/pdf.pdf', 'wb') as f:
                f.write(response.content)
            return True
        else:
            print('Error downloading PDF:', response.status_code)
            return False

    @classmethod
    def convert_pdf_to_images(cls, pdf_path):
        # verify if pdf_path is an url
        if pdf_path.startswith("http"):
            if not cls.save_pdf_in_tmp(pdf_path):
                return None
            pdf_path = '/tmp/pdf.pdf'
        try:
            images = convert_from_path(pdf_path)
            return images
        except Exception as e:
            print('Error converting PDF to images:', e)
            return None
