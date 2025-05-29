import os
from config.wsgi import *
from django.template.loader import get_template
from weasyprint import HTML, CSS
from config import settings

def printTicket():
    template = get_template("ticket.html")
    context = {"name": "First Name User"}
    html_template = template.render(context)

    css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-5.0.0-dist/css/bootstrap.min.css')
    HTML(string=html_template).write_pdf(target="ticket.pdf", stylesheets=[CSS(css_url)])


printTicket()