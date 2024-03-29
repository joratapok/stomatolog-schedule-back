from django.http import HttpResponse
from django.template.loader import get_template
import pdfkit
import os


def render_pdf_view(template_html, params: dict, event):
    template = get_template(template_html)
    html = template.render(params)
    pdf_name = 'invoice.pdf'

    if os.name == 'nt':
        # ------------- For windows settings ------------
        path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        pdfkit.from_string(html, pdf_name, configuration=config, options={"enable-local-file-access": True})
        # ------------ End of windows settings -----------
    else:
        # ------------- For linux settings ------------
        pdfkit.from_string(html, pdf_name)
        # ------------ End of linux settings -----------

    event.invoice.save('invoice.pdf', open(pdf_name, 'rb'))
    pdf = open(pdf_name, 'rb')
    response = HttpResponse(pdf.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={pdf_name}'
    pdf.close()
    os.remove(pdf_name)
    return response
