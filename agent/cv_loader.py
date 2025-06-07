import os
import pdfplumber
from openai_agents import Document


def load_cv():
    """Devuelve una lista de Document con el contenido del CV."""
    docs = []

    if (text := os.getenv("CV_TEXT")):
        docs.append(Document(content=text, metadata={"source": "env"}))

    elif (path := os.getenv("CV_PATH")) and os.path.exists(path):
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                docs.append(Document(content=page.extract_text(), metadata={"source": path}))

    elif (url := os.getenv("CV_URL")):
        import requests, io
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        with pdfplumber.open(io.BytesIO(resp.content)) as pdf:
            for page in pdf.pages:
                docs.append(Document(content=page.extract_text(), metadata={"source": url}))

    else:
        raise RuntimeError(
            "Debes definir CV_TEXT, CV_PATH o CV_URL en variables de entorno para que el bot conozca tu CV."
        )
    return docs