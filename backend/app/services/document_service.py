import os

from pypdf import PdfReader


def extract_text(file_path: str):

    extension = os.path.splitext(
        file_path
    )[1]

    text = ""

    # TXT Files
    if extension == ".txt":

        with open(
                file_path,
                "r",
                encoding="utf-8"
        ) as f:

            text = f.read()

    # PDF Files
    elif extension == ".pdf":

        reader = PdfReader(file_path)

        for page in reader.pages:
            text += page.extract_text()

    return text