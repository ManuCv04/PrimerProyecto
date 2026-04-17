import fitz  # PyMuPDF
import os

carpeta_pdfs = "pdfs"
carpeta_md = "knowledge"

# Crear carpeta si no existe
os.makedirs(carpeta_md, exist_ok=True)

for archivo in os.listdir(carpeta_pdfs):
    if archivo.endswith(".pdf"):
        ruta_pdf = os.path.join(carpeta_pdfs, archivo)
        doc = fitz.open(ruta_pdf)

        texto = ""
        for page in doc:
            texto += page.get_text()

        nombre_md = archivo.replace(".pdf", ".md")
        ruta_md = os.path.join(carpeta_md, nombre_md)

        with open(ruta_md, "w", encoding="utf-8") as f:
            f.write(texto)

        print(f"✅ Convertido: {archivo} → {nombre_md}")