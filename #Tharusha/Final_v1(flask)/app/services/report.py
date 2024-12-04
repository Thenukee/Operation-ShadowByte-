# report.py
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

def generate_pdf_report(suspect_details, results_data):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle(f"Report for {suspect_details.get('name', 'Unknown Suspect')}")

    # Add header
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 750, f"Suspect Report: {suspect_details.get('name', 'N/A')}")
    pdf.setFont("Helvetica", 12)

    # Add suspect details
    y = 720
    for key, value in suspect_details.items():
        pdf.drawString(50, y, f"{key.capitalize()}: {value}")
        y -= 20

    # Add results summary
    y -= 20
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Results Summary:")
    y -= 30
    pdf.setFont("Helvetica", 12)
    for method, items in results_data.items():
        pdf.drawString(50, y, f"{method.capitalize()} ({len(items)} results):")
        y -= 20
        for item in items:
            pdf.drawString(70, y, f"- {item.get('title', 'N/A')}")
            y -= 15
            if y < 50:
                pdf.showPage()
                y = 750
                pdf.setFont("Helvetica", 12)

    pdf.save()
    buffer.seek(0)
    return buffer
