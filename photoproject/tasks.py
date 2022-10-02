from celery import shared_task
from .services.handle_receipt import save_pdf_to_db, save_pdf_for_project_to_db
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Project


@shared_task()
def add(x, y):
    return x + y


@shared_task
def save_pdf(receipt_id):
    save_pdf_to_db(receipt_id)


@shared_task
def send_email_with_receipt(email, receipt_id, receipt_file_document_url):
    message = EmailMessage(
        "Receipt pdf file",
        f"Here is the the pdf for receipt #{receipt_id}",
        "bookingdjangoprojkpi@gmail.com",
        [email],
        headers={"Message-ID": "foo"},
    )
    message.attach_file(str(settings.BASE_DIR) + receipt_file_document_url)

    # message.attach("receipt.pdf", receipt.file_document)
    message.send()


@shared_task
def send_email_to_project_users():

    projects = Project.objects.all()

    for project in projects:

        proj_file_instance = save_pdf_for_project_to_db(project)

        # message = EmailMessage(
        #     "Project receipts file",
        #     f"Here is the the pdf for project_{project.id} reseipts for last week ",
        #     "bookingdjangoprojkpi@gmail.com",
        #     [project.user.email],
        #     headers={"Message-ID": "foo"},
        # )
        # message.attach_file(
        #     str(settings.BASE_DIR) + proj_file_instance.file_document.url
        # )

        # message.send()
    # print("done")


@shared_task
def xsum(numbers):
    return sum(numbers)
