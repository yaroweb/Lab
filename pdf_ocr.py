import sqlalchemy
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import pytesseract
from pdf2image import convert_from_path
import glob
import os
import ollama
import json
import re
from datetime import datetime
import pandas as pd

# Konfigurationsparameter
PDF_FOLDER_PATH = '/your_path'
OUTPUT_JSON_PATH = 'Insolvy_Data.json'

# Datenbank-Verbindung einrichten
DATABASE_URL = f"postgresql://insolvy_user:{quote_plus('yourpassword')}@localhost/insolvency_db"
engine = create_engine(DATABASE_URL)

def pdf_to_text(pdf_path):
    """Konvertiert ein PDF in Text"""
    images = convert_from_path(pdf_path, dpi=300)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img, lang='deu')
    return text

def extract_information(text):
    """Extrahiere relevante Informationen aus dem Text"""
    prompt = f"""
    Extrahiere folgende Informationen im JSON-Format:
    {{
        "Datum_Verfahrenseroeffnung": "{{datum}}",
        "Frist_Forderungsanmeldung": "{{frist}}",
        "Termin_Glaeubigerversammlung": "{{termin}}",
        "Insolvenzverwalter": "{{insolvenzverwalter}}",
        "Glaeubiger": [
            {{"Name": "{{glaeubiger_name}}", "Betrag": "{{betrag}}"}}
        ]
    }}
    
    Text:
    {text}
    """
    response = ollama.chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']

def extract_json_from_response(response_text):
    """Extrahiert JSON aus der AI-Antwort und behebt Formatierungsfehler"""
    try:
        json_text = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_text:
            formatted_text = json_text.group()
            formatted_text = re.sub(r'\b(True|False)\b', lambda m: m.group(0).lower(), formatted_text)  # Fix boolean values
            formatted_text = formatted_text.replace("\n", "")  # Remove newlines
            formatted_text = formatted_text.replace("\t", "")  # Remove tabs
            return json.loads(formatted_text)
        else:
            raise ValueError("Keine gültigen JSON-Daten gefunden.")
    except json.JSONDecodeError as e:
        print("❌ JSON-Fehler beim Parsen:", e)
    except Exception as e:
        print("❌ Fehler beim JSON-Parsing:", e)
    return None

def convert_date_format(date_str):
    """Konvertiert ein deutsches Datumsformat in das richtige SQL-Format (YYYY-MM-DD)"""
    try:
        return datetime.strptime(date_str, "%d.%m.%Y").strftime("%Y-%m-%d")
    except ValueError:
        return None

def save_to_database(data, filename):
    """Speichert extrahierte Daten in die Datenbank"""
    try:
        with engine.connect() as conn:
            conn.execute(
                text("""
                INSERT INTO insolvency_cases (
                    quelle,
                    datum_verfahrenseroeffnung,
                    frist_forderungsanmeldung,
                    termin_glaeubigerversammlung,
                    insolvenzverwalter,
                    glaeubiger
                ) VALUES (:quelle, :datum_verfahrenseroeffnung, :frist_forderungsanmeldung, :termin_glaeubigerversammlung, :insolvenzverwalter, :glaeubiger)
                """),
                {
                    'quelle': filename,
                    'datum_verfahrenseroeffnung': convert_date_format(data.get('Datum_Verfahrenseroeffnung', 'N/A')),
                    'frist_forderungsanmeldung': convert_date_format(data.get('Frist_Forderungsanmeldung', 'N/A')),
                    'termin_glaeubigerversammlung': convert_date_format(data.get('Termin_Glaeubigerversammlung', 'N/A')),
                    'insolvenzverwalter': json.dumps(data.get('Insolvenzverwalter', {})),  # Convert dictionary to JSON string
                    'glaeubiger': json.dumps(data.get('Glaeubiger', []))
                }
            )
            conn.commit()
        print(f"✅ {filename} erfolgreich gespeichert.")
    except Exception as e:
        print(f"❌ Fehler beim Speichern in die Datenbank für {filename}: {e}")

def display_saved_data():
    """Zeigt die gespeicherten Daten aus der Datenbank als Tabelle an"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM insolvency_cases"))
            rows = result.fetchall()
            columns = result.keys()
            df = pd.DataFrame(rows, columns=columns)
            print("\n📊 Gespeicherte Daten in der Datenbank:")
            print(df)
    except Exception as e:
        print(f"❌ Fehler beim Abrufen der Daten: {e}")

def process_pdfs(pdf_folder):
    """Verarbeitet alle PDFs im angegebenen Ordner"""
    pdf_files = glob.glob(os.path.join(pdf_folder, '*.pdf'))
    for pdf_file in pdf_files:
        print(f"\n🔍 Verarbeitung {os.path.basename(pdf_file)}")
        text = pdf_to_text(pdf_file)
        extracted_json = extract_information(text)
        data = extract_json_from_response(extracted_json)
        
        if data:
            save_to_database(data, os.path.basename(pdf_file))
        else:
            print(f"❌ Keine gültigen JSON-Daten bei {os.path.basename(pdf_file)}.")

if __name__ == "__main__":
    process_pdfs(PDF_FOLDER_PATH)
    display_saved_data()
