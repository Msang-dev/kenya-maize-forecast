from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_report(
    county,
    production,
    risk,
    output_file
):

    pdf = canvas.Canvas(
        output_file,
        pagesize=letter
    )

    pdf.drawString(
        50,
        750,
        "Kenya Maize Forecast Report"
    )

    pdf.drawString(
        50,
        720,
        f"County: {county}"
    )

    pdf.drawString(
        50,
        700,
        f"Forecast Production: {production:,.0f}"
    )

    pdf.drawString(
        50,
        680,
        f"Climate Risk: {risk}"
    )

    pdf.save()

    return output_file