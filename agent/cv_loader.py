"""Carga el CV desde ENV, PDF local o URL y lo devuelve como texto plano."""

import os
import io
import pdfplumber
import requests


def load_cv() -> str:
    """Devuelve TODO el texto del CV como una única cadena."""

    # 1️⃣ Variable de entorno con el texto directamente
    if (text := os.getenv("CV_TEXT")):
        return text

    # 2️⃣ PDF en el contenedor
    if (path := os.getenv("CV_PATH")) and os.path.exists(path):
        with pdfplumber.open(path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)

    # 3️⃣ PDF remoto por URL
    if (url := os.getenv("CV_URL")):
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        with pdfplumber.open(io.BytesIO(resp.content)) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)

    # Si nada aplica → error explícito
    raise RuntimeError(
        "Debes definir CV_TEXT, CV_PATH o CV_URL para que el bot conozca tu CV."
    )
