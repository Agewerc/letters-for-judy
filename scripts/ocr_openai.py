import os
import re
import base64
import json
from io import BytesIO
from PIL import Image
from tqdm import tqdm
from openai import OpenAI
from pdf2image import convert_from_path

client = OpenAI()

def encode_image(image_path):
    """Convert image file to base64 string."""
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

def clean_json_output(raw_output):
    """Remove triple backticks and language hints like ```json."""
    if not raw_output:
        return raw_output
    cleaned = re.sub(r"^```(?:json)?\s*", "", raw_output.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()

def ocr_with_openai(image_path, relative_path):
    """Extract structured OCR data from an image using OpenAI."""
    base64_image = encode_image(image_path)

    prompt = (
        "A carta nesta imagem está escrita em português. "
        "Extraia cuidadosamente o texto mantendo ortografia e pontuação originais. "
        "Tente identificar:\n"
        "1. Quem escreveu a carta ('from')\n"
        "2. Para quem foi escrita ('to')\n"
        "3. Data da carta, se visível ('date')\n"
        "4. Texto completo da carta ('text')\n\n"
        "Responda estritamente em JSON no formato:\n"
        "{\n"
        "  \"from\": \"Nome de quem escreveu ou null\",\n"
        "  \"to\": \"Nome do destinatário ou null\",\n"
        "  \"date\": \"DD/MM/AAAA ou null\",\n"
        "  \"text\": \"Transcrição completa\",\n"
        "  \"image_path\": \"CAMINHO_RELATIVO_DA_IMAGEM\"\n"
        "}"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é um arquivista especializado em cartas antigas escritas em português."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt.replace("CAMINHO_RELATIVO_DA_IMAGEM", relative_path)},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        temperature=0
    )

    raw_output = response.choices[0].message.content
    print("\n--- RAW MODEL OUTPUT ---\n")
    print(raw_output)
    print("\n------------------------\n")

    cleaned_output = clean_json_output(raw_output)

    try:
        return json.loads(cleaned_output)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        print("Cleaned output:\n", cleaned_output)
        raise ValueError("OpenAI did not return valid JSON")

def convert_pdf_to_images(pdf_path, temp_dir="archive/temp_images"):
    """Convert PDF to JPEG images."""
    os.makedirs(temp_dir, exist_ok=True)
    images = convert_from_path(pdf_path, dpi=300)
    image_paths = []
    for i, img in enumerate(images):
        img_filename = os.path.join(temp_dir, f"{os.path.splitext(os.path.basename(pdf_path))[0]}_page{i+1}.jpg")
        img.save(img_filename, "JPEG")
        image_paths.append(img_filename)
    return image_paths

def process_all_files(input_dir="archive/originals", output_json="archive/letters.json"):
    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    supported_images = (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp")
    supported_pdfs = (".pdf",)

    all_letters = []

    files = [f for f in os.listdir(input_dir) if f.lower().endswith(supported_images + supported_pdfs)]

    for filename in tqdm(files, desc="OpenAI OCR (Portuguese letters)"):
        file_path = os.path.join(input_dir, filename)

        try:
            if filename.lower().endswith(supported_pdfs):
                # Convert PDF pages to images and OCR each
                image_paths = convert_pdf_to_images(file_path)
                for img_path in image_paths:
                    rel_path = os.path.relpath(img_path, start=".")
                    data = ocr_with_openai(img_path, rel_path)
                    all_letters.append(data)
            else:
                # Process image directly
                rel_path = os.path.relpath(file_path, start=".")
                data = ocr_with_openai(file_path, rel_path)
                all_letters.append(data)

        except Exception as e:
            tqdm.write(f"❌ Error processing {filename}: {e}")

    # Save as JSON
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(all_letters, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(all_letters)} letters to {output_json}")

if __name__ == "__main__":
    process_all_files()
