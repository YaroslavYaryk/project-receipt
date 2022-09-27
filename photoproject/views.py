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


@login_required(login_url="login")
def index(request):

    my_receipts = handle_receipt.get_receipts_by_user(request.user)

    context = {"my_receipts": my_receipts}

    return render(request, "photo/home.html", context)


def send(request):

    send_mail(
        "Subject here",
        "Here is the message.",
        "bookingdjangoprojkpi@gmail.com",
        ["duhanov2003@gmail.com"],
        fail_silently=False,
    )

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
            handle_receipt.save_pdf_to_db(receipt.id)

            return redirect("home")

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
            handle_receipt.save_pdf_to_db(receipt_id)
            return redirect("home")

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


# , 'content','getvalue', 'has_header', 'headers', 'items', 'make_bytes', 'readable', 'reason_phrase', 'seekable', 'serialize', 'serialize_headers', 'set_cookie', 'set_signed_cookie', 'setdefault', 'status_code', 'streaming', 'tell', 'writable', 'write', 'writelines'


def excel_layout(request, receipt_id):
    receipt = handle_receipt.get_receipt_by_id(receipt_id)

    return render(
        request,
        "static/excel_layout.html",
        {"receipt": receipt, "a": list(range(13)), "b": list(range(27))},
    )
