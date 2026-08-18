from decouple import config
import firebase_admin
from firebase_admin import credentials, storage
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
cred_path = BASE_DIR / config('FIREBASE_CREDENTIALS_PATH')



try:
    cred = credentials.Certificate(str(cred_path))
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred, {
            'storageBucket': config('FIREBASE_STORAGE_BUCKET')
        })

    bucket = storage.bucket()
    blob = bucket.blob("prueba.txt")
    blob.upload_from_string("Test de conexión")

    print(True, ", se logró la conexión")

except Exception as e:
    print(False)
    print("Error:", e)


