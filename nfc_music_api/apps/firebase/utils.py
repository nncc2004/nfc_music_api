import os
import uuid
from pathlib import Path
from urllib.parse import urlparse

import firebase_admin
from decouple import config
from firebase_admin import credentials, storage


BASE_DIR = Path(__file__).resolve().parent

cred_path = os.path.join(
    BASE_DIR,
    "..",
    config("FIREBASE_CREDENTIALS_PATH")
)

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)

    firebase_admin.initialize_app(cred, {
        "storageBucket": config("FIREBASE_STORAGE_BUCKET"),
    })

bucket = storage.bucket()

'''
Funciones de utilidad
'''

def subir_archivo_firebase(archivo_django_file, carpeta="nfc_music_files"):
    """
    Sube un archivo a Firebase Storage y devuelve su URL pública.
    """
    nombre = f"{uuid.uuid4()}.mp3"
    ruta_firebase = f"{carpeta}/{nombre}"

    try:
        blob = bucket.blob(ruta_firebase)

        blob.upload_from_file(
            archivo_django_file,
            content_type="audio/mpeg"
        )

        blob.make_public()

        return blob.public_url

    except Exception as e:
        print(f"Error subiendo archivo a Firebase: {e}")
        return None


def obtener_ruta_firebase(url):
    """
    Extrae la ruta interna de un archivo Firebase Storage
    desde su URL pública.
    """
    try:
        partes = urlparse(url)
        partes_path = partes.path.strip("/").split("/")

        if len(partes_path) >= 2:
            return "/".join(partes_path[1:])

        return None

    except Exception as e:
        print(f"Error extrayendo ruta de Firebase: {e}")
        return None


def eliminar_archivo_firebase(url):
    """
    Elimina un archivo de Firebase Storage a partir de su URL pública.
    """
    try:
        ruta = obtener_ruta_firebase(url)

        if not ruta:
            print(f"No se pudo obtener la ruta desde: {url}")
            return False

        blob = bucket.blob(ruta)
        blob.delete()

        return True

    except Exception as e:
        print(f"Error eliminando archivo de Firebase: {e}")
        return False