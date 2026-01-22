import tempfile
import shutil
from contextlib import contextmanager

@contextmanager
def ephemeral_file(upload):
    suffix = ""
    if upload.filename and "." in upload.filename:
        suffix = "." + upload.filename.split(".")[-1]

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp.write(upload.file.read())
    temp.close()

    try:
        yield temp.name
    finally:
        shutil.os.remove(temp.name)
