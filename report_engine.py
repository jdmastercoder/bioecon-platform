import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def generate_pdf_report(disease_choice, sim_results, alloc_v, alloc_b, alloc_t):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36,
                            leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()

    # Title
    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['Heading1'], fontSize=20, leading=24, textColor=colors.HexColor('#1E3A8A'))
    story.append(
        Paragraph("BioEcon Executive Decision Support Report", title_style))
    story.append(Spacer(1, 12))

    # Summary Text
    body_style = styles['Normal']
    summary_text = f"<b>Pathogen Selected:</b> {disease_choice}<br/>" \
        f"<b>Peak Active Infections:</b> {int(max(sim_results['infected'])):,}<br/>" \
        f"<b>Peak Hospital ICU Demand:</b> {sim_results['peak_hospitalizations']:,} beds (Day {sim_results['peak_day']})"
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 16))

    # Allocation Table Data
    table_data = [
        ["Facility Name", "Capacity Share",
            "Vaccine Doses", "ICU Beds", "Treatments"],
        ["Lakeridge Health Oshawa", "45%",
            f"{int(alloc_v*0.45):,}", f"{int(alloc_b*0.45):,}", f"{int(alloc_t*0.45):,}"],
        ["Lakeridge Health Ajax Pickering", "25%",
            f"{int(alloc_v*0.25):,}", f"{int(alloc_b*0.25):,}", f"{int(alloc_t*0.25):,}"],
        ["Lakeridge Health Whitby", "15%",
            f"{int(alloc_v*0.15):,}", f"{int(alloc_b*0.15):,}", f"{int(alloc_t*0.15):,}"],
        ["Lakeridge Health Bowmanville", "15%",
            f"{int(alloc_v*0.15):,}", f"{int(alloc_b*0.15):,}", f"{int(alloc_t*0.15):,}"],
    ]

    t = Table(table_data, colWidths=[180, 80, 90, 80, 90])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
         [colors.white, colors.HexColor('#F8FAFC')]),
    ]))

    story.append(t)
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
