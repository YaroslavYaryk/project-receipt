from calendar import c
import imp
from django.contrib import messages
from .forms import ReceiptForm, ProjectForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect
from .services import handle_receipt
import json
import csv
from django.utils.encoding import smart_str
from django.http.response import HttpResponse
import xlwt
from decouple import config
from django.conf import settings
import os
from pdfrw import PdfWriter
import io
from django.core.files import File
from csv2pdf import convert
from PhotoProject.celery import debug_task
from .tasks import save_pdf, send_email_with_receipt
from django.core.mail import EmailMessage
import requests


@login_required(login_url="login")
def index(request):
    my_receipts = handle_receipt.get_receipts_by_user(request.user)

    send_mail = request.COOKIES.get("send_mail")

    context = {"my_receipts": my_receipts, "cookie": send_mail}

    response = render(request, "photo/home.html", context)

    response.delete_cookie("send_mail")

    return response


@login_required(login_url="login")
def send_receipt_to_email(request, email, receipt_id):

    receipt = handle_receipt.get_receipt_by_id(receipt_id)

    send_email_with_receipt.delay(email, receipt_id, receipt.file_document.url)

    return redirect("home")


@login_required(login_url="login")
def create_receipt(request):

    # categories with aditional "other" value
    special_categories = handle_receipt.get_category_aditional_queryser()
    special_projects = handle_receipt.get_projects_aditional_queryset(request.user)
    if request.method == "POST":
        form = ReceiptForm(request.POST)

        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.user = request.user
            handle_receipt.save_category(receipt, request.POST)
            handle_receipt.save_project(receipt, request.POST)

            handle_receipt.save_images(receipt, request.FILES)
            # print(form.cleaned_data, form.is_valid(), request.POST, request.FILES)
            receipt.save()
            save_pdf.delay(receipt.id)

            response = redirect("home")

            response.set_cookie("send_mail", receipt.id)

            return response

        else:
            messages.error(request, form.errors)

    form = ReceiptForm()

    context = {
        "form": form,
        "categories": special_categories,
        "projects": special_projects,
    }

    return render(request, "photo/create_receipt.html", context)


@login_required(login_url="login")
def create_project(request):

    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            elem = form.save(commit=False)
            elem.user = request.user
            elem.save()
            return redirect("get_projects_list")
        else:
            messages.error(request, form.errors)

    form = ProjectForm()

    context = {"form": form}

    return render(request, "photo/create_project.html", context)


@login_required(login_url="login")
def edit_project(request, project_id):

    project = handle_receipt.get_project_by_id(project_id)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()
            return redirect("get_projects_list")
        else:
            messages.error(request, form.errors)

    form = ProjectForm(instance=project)

    context = {"form": form}

    return render(request, "photo/edit_project.html", context)


@login_required(login_url="login")
def delete_project(request, project_id):

    try:
        handle_receipt.get_project_by_id(project_id).delete()
    except Exception as ex:
        messages.error(request, ex)
        print(ex)
    return redirect("get_projects_list")


@login_required(login_url="login")
def get_projects_list(request):

    users_projects = handle_receipt.get_projects_for_user(request.user)

    context = {"projects": users_projects}

    return render(request, "photo/projects.html", context)


@login_required(login_url="login")
def edit_receipt(request, receipt_id):

    # categories with aditional "other" value
    receipt = handle_receipt.get_receipt_by_user(receipt_id)
    special_categories = handle_receipt.get_category_aditional_queryser()
    special_projects = handle_receipt.get_projects_aditional_queryset(request.user)
    if request.method == "POST":
        form = ReceiptForm(request.POST, instance=receipt)

        if form.is_valid():
            receipt = form.save(commit=False)
            handle_receipt.save_category(receipt, request.POST)
            handle_receipt.save_project(receipt, request.POST)

            handle_receipt.save_edit_images(receipt, request.FILES)
            # print(form.cleaned_data, form.is_valid(), request.POST, request.FILES)
            receipt.save()
            save_pdf.delay(receipt.id)
            # handle_receipt.save_pdf_to_db(receipt_id)
            response = redirect("home")

            # response = handle_receipt.get_download_response(receipt)

            response.set_cookie("send_mail", receipt.id)

            return response

        else:
            messages.error(request, form.errors)

    form = ReceiptForm(instance=receipt)

    context = {
        "form": form,
        "categories": special_categories,
        "projects": special_projects,
        "receipt": receipt,
    }

    return render(request, "photo/edit_receipt.html", context)


@login_required(login_url="login")
def delete_receipt(request, receipt_id):

    receipt = handle_receipt.get_receipt_by_user(receipt_id)
    try:
        handle_receipt.delete_receipt_and_components(receipt)
    except Exception as ex:
        messages.error(request, ex)
        print(ex)
    return redirect("home")


@login_required(login_url="login")
def download_receipt(request, receipt_id):

    receipt = handle_receipt.get_receipt_by_user(receipt_id)
    try:
        response = handle_receipt.get_download_response(receipt)
        return response
    except Exception as ex:
        messages.error(request, ex)
        print(ex)
    return redirect("home")


# , 'content','getvalue', 'has_header', 'headers', 'items', 'make_bytes', 'readable', 'reason_phrase', 'seekable', 'serialize', 'serialize_headers', 'set_cookie', 'set_signed_cookie', 'setdefault', 'status_code', 'streaming', 'tell', 'writable', 'write', 'writelines'


def excel_layout(request, project_id):
    project = handle_receipt.get_project_by_id(project_id)
    print(project)
    receipts = handle_receipt.get_receipts_for_project(project)
    print(receipts)
    total_price = sum(el.price for el in receipts)
    return render(
        request,
        "static/excel_project.html",
        {
            "project": project,
            "a": list(range(13)),
            "total_price": total_price,
            "receipts": receipts,
            "b": list(range(27)),
        },
    )
