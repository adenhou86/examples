import openai
import base64
from pdf2image import convert_from_path
from PIL import Image
import os

# === CONFIGURATION ===
openai.api_key = "YOUR_API_KEY"
PDF_PATH = "your_doc.pdf"
NUM_PAGES_TO_SEND = 5
DPI = 400
TEMP_DIR = "temp_pages"

os.makedirs(TEMP_DIR, exist_ok=True)

# === STEP 1: Convert PDF to high-res images ===
print("Converting PDF to images...")
pages = convert_from_path(PDF_PATH, dpi=DPI)
image_paths = []

for i, page in enumerate(pages[:NUM_PAGES_TO_SEND]):
    img_path = os.path.join(TEMP_DIR, f"page_{i+1}.png")
    page.save(img_path, "PNG")
    image_paths.append(img_path)

# === STEP 2: Encode images to base64 ===
def encode_image(file_path):
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# === STEP 3: Prepare GPT-4o message ===
messages = [
    {
        "role": "system",
        "content": "You are an expert financial analyst. Analyze the following report images and answer the user question."
    },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "Based on the following 5 image pages, what is the trend in net interest income and the exposure breakdown?"}
        ] + [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{encode_image(path)}",
                    "detail": "auto"
                }
            } for path in image_paths
        ]
    }
]

# === STEP 4: Query GPT-4o ===
print("Querying GPT-4o...")
response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=messages,
    temperature=0.3
)

# === OUTPUT ===
print("\n🔍 GPT-4o Answer:")
print(response.choices[0].message["content"])
