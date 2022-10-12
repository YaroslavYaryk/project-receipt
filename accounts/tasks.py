from celery import shared_task
from django.core.mail import EmailMessage, send_mail
from django.template.loader import get_template
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from decouple import config


@shared_task
def send_reset_password_email(token, email):
    email_plaintext_message = get_template("photo/product.html").render(
        {
            "token": token,
            # "image": f"{config('HOST')}:{config('PORT')}{settings.STATIC_URL + 'images/restaurant.jpg'}",
        }
    )
    html_message = render_to_string("photo/product.html", {"token": token})
    plain_message = strip_tags(html_message)

    # mail = EmailMessage(
    #     subject="Password reset confirmation",
    #     body=email_plaintext_message,
    #     to=[email],
    #     # reply_to=[EMAIL_ADMIN],
    # )
    # mail.content_subtype = "html"
    # mail.send()

    send_mail(
        "Password reset confirmation",
        plain_message,
        config("EMAIL_HOST_USER"),
        [email],
        html_message=html_message,
    )
