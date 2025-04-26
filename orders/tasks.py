from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order
from celery import shared_task 
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id):
    """task to send e-mail notifications when an order is placed successfully"""
    order = Order.objects.get(id=order_id)

    # Subject for both emails
    subject = f'Order nr. {order.id}'

    # Message for the customer
    user_message = f'Dear {order.first_name},\n\n' \
                   f'You have successfully placed an order.\n' \
                   f'Your order ID is {order.id}.'

    # Message for the admin
    admin_message = f'New order has been placed.\n\n' \
                    f'Order ID: {order.id}\n' \
                    f'Customer Name: {order.first_name} {order.last_name}\n' \
                    f'Customer Email: {order.email}\n' \
                    f'Order Details (razorpay link): {order.get_order_url()} (This can be adjusted as per your model)'

    # List of recipients for both the user and the admin
    user_recipient = [order.email]
    admin_recipient = [settings.ADMIN_EMAIL]

    # Send the email to the customer
    send_mail(
        subject,
        user_message,
        'goodluckflorist@gmail.com',  # From email
        user_recipient  # To the customer's email
    )

    # Send the email to the admin
    mail_sent = send_mail(
        subject,
        admin_message,
        'goodluckflorist@gmail.com',  # From email
        admin_recipient  # To the admin's email
    )

    return mail_sent

@shared_task
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully paid.
    """
    order = Order.objects.get(id=order_id)
    # create invoice e-mail
    subject = f'My Shop - Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject,message,'goodluckflorist@gmail.com',[order.email])
    # generate PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets=[weasyprint.CSS(settings.BASE_DIR / 'static/css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,stylesheets=stylesheets)
    # attach PDF file
    email.attach(f'order_{order.id}.pdf',out.getvalue(),'application/pdf')
    # send e-mail
    email.send()