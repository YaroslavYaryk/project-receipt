from photoproject.models import Category, Photo, Project, Receipt, ProjectReceipts
from django.utils.text import slugify
from django.conf import settings
import os
from pdfrw import PdfWriter
import io
from django.core.files import File
from csv2pdf import convert
from django.utils.encoding import smart_str
from django.http.response import HttpResponse
import csv
from io import BytesIO
from django.core.files import File
from photoproject.utils import render_to_pdf
from weasyprint import HTML, CSS
from django.core.files.uploadedfile import SimpleUploadedFile
from django.template.loader import get_template
from datetime import date


HTML_DIRECTORY = os.path.join(settings.BASE_DIR, "media/htmls")
PDF_DIRECTORY = os.path.join(settings.BASE_DIR, "media/pdfs")
PDF_MEDIA_RELATED = "/pdfs"


def get_category_aditional_queryser():
    return (
        [("------------------", "---------------")]
        + [(el.name, el.name) for el in Category.objects.all()]
        + [("other", "other")]
    )


def get_category_by_name(name):
    try:
        return Category.objects.get(name=name)
    except:
        return None


def get_project_by_name(name):
    try:
        return Project.objects.get(name=name)
    except:
        return None


def handle_create_category(name):
    return Category.objects.get_or_create(name=name, slug=slugify(name))[0]


def handle_create_project(name, user):
    return Project.objects.get_or_create(name=name, user=user)[0]


def save_category(receipt, data):
    if get_category_by_name(data.get("categories")):
        category = get_category_by_name(data.get("categories"))

    elif data.get("category-input"):
        category = handle_create_category(data.get("category-input"))

    receipt.category = category
    receipt.save()


def save_project(receipt, data):
    if get_project_by_name(data.get("projects")):
        project = get_project_by_name(data.get("projects"))

    elif data.get("project-input"):
        project = handle_create_project(data.get("project-input"), receipt.user)

    receipt.project = project
    receipt.save()


def save_images(receipt, files):
    if files.get("photos"):
        for image in files.getlist("photos"):
            receipt.photos.add(Photo.objects.create(photo=image))

    receipt.save()


def delete_receipt_photos(receipt):
    for image in receipt.photos.all():
        image.delete()


def save_edit_images(receipt, files):
    if files.get("photos"):
        delete_receipt_photos(receipt)
        for image in files.getlist("photos"):
            receipt.photos.add(Photo.objects.create(photo=image))

    receipt.save()


def get_receipts_by_user(user):
    return Receipt.objects.filter(user=user)


def get_projects_for_user(user):
    return Project.objects.filter(user=user)


def get_projects_aditional_queryset(user):
    return (
        [("------------------", "---------------")]
        + [(el.name, el.name) for el in Project.objects.filter(user=user)]
        + [("other", "other")]
    )


def get_receipt_by_user(receipt_id):
    return Receipt.objects.get(pk=receipt_id)


def delete_receipt_and_components(receipt):

    delete_receipt_photos(receipt)
    receipt.delete()


def get_project_by_id(project_id):
    return Project.objects.get(pk=project_id)


def get_receipt_by_id(receipt_id):
    return Receipt.objects.get(pk=receipt_id)


def writer_write_row(writer, receipt):
    writer.writerow(
        [
            smart_str("Company: "),
            smart_str(receipt.company),
            smart_str(" "),
            smart_str(" "),
            smart_str(" "),
        ]
    )
    writer.writerow(
        [
            smart_str("Project: "),
            smart_str(receipt.project.name),
            smart_str(" "),
            smart_str(" "),
            smart_str(" "),
        ]
    )
    writer.writerow(
        [
            smart_str(" "),
            smart_str(" "),
            smart_str(" "),
            smart_str(" "),
            smart_str(" "),
        ]
    )
    writer.writerow(
        [
            smart_str("Submitter "),
            smart_str(" "),
            smart_str(" "),
            smart_str(" "),
            smart_str(" "),
        ]
    )
    writer.writerow(
        [
            smart_str("Name: "),
            smart_str(receipt.user.name),
            smart_str(" "),
            smart_str(" "),
            smart_str(" "),
        ]
    )
    writer.writerow(
        [
            smart_str("Phone: "),
            smart_str(receipt.user.phone),
            smart_str(" "),
            smart_str(" "),
            smart_str(" "),
        ]
    )
    writer.writerow(
        [
            smart_str(" "),
            smart_str(" "),
            smart_str(" "),
            smart_str(" "),
            smart_str(" "),
        ]
    )
    writer.writerow(
        [
            smart_str("Reimburser "),
            smart_str(" "),
            smart_str(" "),
            smart_str(" "),
            smart_str(" "),
        ]
    )
    writer.writerow(
        [
            smart_str("Name: "),
            smart_str(receipt.user.name),
            smart_str(" "),
            smart_str(" "),
            smart_str(" "),
        ]
    )
    writer.writerow(
        [
            smart_str("Phone: "),
            smart_str(receipt.user.phone),
            smart_str(" "),
            smart_str(" "),
            smart_str(" "),
        ]
    )
    writer.writerow(
        [
            smart_str("Account number: "),
            smart_str(receipt.user.account_number),
            smart_str(" "),
            smart_str(" "),
            smart_str(" "),
        ]
    )
    writer.writerow(
        [
            smart_str(" "),
            smart_str(" "),
            smart_str(" "),
            smart_str(" "),
            smart_str(" "),
        ]
    )

    writer.writerow(
        [
            smart_str("Date "),
            smart_str("Description"),
            smart_str("Category"),
            smart_str("People"),
            smart_str("Sum"),
        ]
    )


def save_pdf_to_db(receipt_id):

    receipt = get_receipt_by_id(receipt_id)

    html_template = get_template("static/excel_layout.html")
    # user = request.user
    # print(html_template, "here")
    rendered_html = html_template.render({"receipt": receipt})

    pdf_file = HTML(string=rendered_html).write_pdf()

    receipt.file_document = SimpleUploadedFile(
        f"receipt_{receipt_id}.pdf",
        pdf_file,
        content_type="application/pdf",
    )
    receipt.save()


def get_download_response(receipt):
    file_location = str(settings.BASE_DIR) + receipt.file_document.url

    # response1 = requests.get(f"{config('HOST')}:{config('PORT')}{receipt.file_document.url}")
    # # response = requests.get(pdf.url_link)
    with open(file_location, "rb") as f:
        file_data = f.read()
        response = HttpResponse(
            file_data,
            content_type="application/pdf",
        )
        response[
            "Content-Disposition"
        ] = f'attachment; filename="receipt_{receipt.id}.pdf"'

    return response


def get_receipts_for_project(project):
    return Receipt.objects.filter(project=project)


def writer_project_write_row(writer, project):

    writer.writerow(
        [
            smart_str("Project: "),
            smart_str(project.name),
            smart_str(" "),
            smart_str(" "),
            smart_str(" "),
        ]
    )
    writer.writerow(
        [
            smart_str(" "),
            smart_str(" "),
            smart_str(" "),
            smart_str(" "),
            smart_str(" "),
        ]
    )

    writer.writerow(
        [
            smart_str("Date "),
            smart_str("Description"),
            smart_str("Category"),
            smart_str("People"),
            smart_str("Sum"),
        ]
    )


def save_pdf_for_project_to_db(project):

    receipts = get_receipts_for_project(project)
    html_template = get_template("static/excel_project.html")
    total_price = sum(el.price for el in receipts)
    rendered_html = html_template.render(
        {"project": project, "receipts": receipts, "total_price": total_price}
    )

    pdf_file = HTML(string=rendered_html).write_pdf()

    proj_file_instance = ProjectReceipts.objects.create(
        project=project,
        file_document=SimpleUploadedFile(
            f"project_{project.id}_{date.today()}.pdf",
            pdf_file,
            content_type="application/pdf",
        ),
    )

    return proj_file_instance
