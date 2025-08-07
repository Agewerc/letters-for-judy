import os
import re
import base64
import json
from io import BytesIO
from PIL import Image
from tqdm import tqdm
from openai import OpenAI
from pdf2image import convert_from_path
import random

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
        "A imagem fornecida pode ser uma carta escrita em português, uma foto, ou outro tipo de documento. "
        "Analise cuidadosamente e responda estritamente em JSON, seguindo estas instruções:\n"
        "1. Se NÃO for uma carta (por exemplo, for uma foto, página em branco, ou outro tipo de documento), defina o campo 'is_letter' como false.\n"
        "2. Se for uma carta, defina 'is_letter' como true e extraia:\n"
        "   - Quem escreveu a carta ('from')\n"
        "   - Para quem foi escrita ('to')\n"
        "   - Data da carta, se visível ('date')\n"
        "   - Texto completo da carta ('text')\n"
        "3. O campo 'date' deve estar sempre no formato DD/MM/AAAA (exemplo: 05/08/2025) ou null se não houver data.\n"
        "4. Mantenha ortografia e pontuação originais do texto.\n"
        "5. Sempre inclua o campo 'image_path' com o caminho relativo da imagem.\n\n"
        "Formato de resposta:\n"
        "{\n"
        "  \"is_letter\": true ou false,\n"
        "  \"from\": \"Nome de quem escreveu ou null\",\n"
        "  \"to\": \"Nome do destinatário ou null\",\n"
        "  \"date\": \"DD/MM/AAAA ou null\",\n"
        "  \"text\": \"Transcrição completa ou null\",\n"
        "  \"image_path\": \"CAMINHO_RELATIVO_DA_IMAGEM\"\n"
        "}"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
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

def process_all_files(input_dir="archive/originals", output_json="archive/letters.json"):

    # Update: Only process .jpg files from local data/all_letters directory
    input_dir = "data/all_letters"  # Local directory with all jpg files
    output_json = "data/letters.json"  # Output for classified letters
    output_strange = "data/strange.json"  # Output for strange/unclassified
    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    supported_images = (".jpg",)

    all_letters = []
    strange_letters = []

    files = [f for f in os.listdir(input_dir) if f.lower().endswith(supported_images)]

    for filename in tqdm(files, desc="OpenAI OCR (Portuguese letters)"):
        file_path = os.path.join(input_dir, filename)
        try:
            rel_path = os.path.relpath(file_path, start=".")
            data = ocr_with_openai(file_path, rel_path)
            # Use AI's is_letter flag and date format for classification
            is_letter = data.get("is_letter", None)
            date_val = data.get("date")
            # Accept only DD/MM/YYYY or null for date
            valid_date = False
            if date_val:
                import re
                valid_date = bool(re.match(r"^\d{2}/\d{2}/\d{4}$", date_val))
            if is_letter is False or not is_letter:
                strange_letters.append(data)
            elif not data.get("text") or not data["text"].strip() or len(data["text"].strip()) < 20 or not valid_date:
                strange_letters.append(data)
            else:
                all_letters.append(data)
        except Exception as e:
            tqdm.write(f"❌ Error processing {filename}: {e}")
            strange_letters.append({
                "is_letter": None,
                "from": None,
                "to": None,
                "date": None,
                "text": None,
                "image_path": rel_path,
                "error": str(e)
            })

    # Save as JSON
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(all_letters, f, ensure_ascii=False, indent=2)

    with open(output_strange, "w", encoding="utf-8") as f:
        json.dump(strange_letters, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(all_letters)} letters to {output_json}")
    print(f"✅ Saved {len(strange_letters)} strange/unclassified items to {output_strange}")

if __name__ == "__main__":
    process_all_files()
