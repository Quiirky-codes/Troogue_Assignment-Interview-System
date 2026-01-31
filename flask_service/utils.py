# flask_service/utils.py
import os
from werkzeug.utils import secure_filename
from datetime import datetime

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_file(file_storage):
    filename = secure_filename(file_storage.filename)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    path = os.path.join(UPLOAD_DIR, f"{timestamp}_{filename}")
    file_storage.save(path)
    return path
