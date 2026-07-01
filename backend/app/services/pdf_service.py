import os

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_redacted_pdf(
        output_path: str,
        text: str
):
    """
    Create a valid PDF containing the redacted text.
    """

    pdf = canvas.Canvas(
        output_path,
        pagesize=letter
    )

    width, height = letter

    y = height - 50

    for line in text.split("\n"):

        pdf.drawString(
            50,
            y,
            line
        )

        y -= 18

        # Start a new page if needed
        if y < 50:

            pdf.showPage()

            y = height - 50

    pdf.save()