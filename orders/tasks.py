from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order
from celery import shared_task 
from .models import Order


@shared_task
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully paid.
    """
    order = Order.objects.get(id=order_id)
    # create invoice e-mail
    subject = f'Order placed at Goodluck Florist - Order no. {order.id}'
    message = "Thank you for your recent purchase!\n We're happy to inform you that your invoice is attached."
    email = EmailMessage(subject,message,'goodluckflorist@gmail.com',[order.email,settings.ADMIN_EMAIL])
    # generate PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets=[weasyprint.CSS(settings.BASE_DIR / 'static/css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,stylesheets=stylesheets)
    # attach PDF file
    email.attach(f'order_{order.id}.pdf',out.getvalue(),'application/pdf')
    # send e-mail
    email.send()