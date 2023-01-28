import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


def link_callback(uri, rel):
    """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    print('PATH ===', path)
    return path
#
#
# def fetch_pdf_resources(uri, rel):
#     if uri.find(settings.MEDIA_URL) != -1:
#         path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
#     elif uri.find(settings.STATIC_URL) != -1:
#         path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ''))
#     else:
#         path = None
#     print('path = ', path)
#     return path
#
#
# def render_pdf_view(request, pdf_template, pdf_context):
#     template_path = pdf_template
#     context = pdf_context
#     # Create a Django response object, and specify content_type as pdf
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(context)
#     print('STATIC = ', settings.STATIC_ROOT)
#     # create a pdf
#     pisa_status = pisa.CreatePDF(
#         html.encode('UTF-16'), dest=response, link_callback=link_callback)
#     # if error then show some funny view
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response


from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa


# def render_pdf_view(path: str, params: dict):
#     template = get_template(path)
#     html = template.render(params)
#     response = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response, encoding='UTF-8', link_callback=link_callback)
#     if not pdf.err:
#         return HttpResponse(response.getvalue(), content_type='application/pdf')
#     else:
#         return HttpResponse("Error Rendering PDF", status=400)
import pdfkit

def render_pdf_view(path: str, params: dict):
    template = get_template(path)
    html = template.render(params)
    response = BytesIO()
    pdf = pdfkit.from_file(BytesIO(html.encode("UTF-8")), 'out.pdf')
    if not pdf.err:
        return HttpResponse(response.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("Error Rendering PDF", status=400)

