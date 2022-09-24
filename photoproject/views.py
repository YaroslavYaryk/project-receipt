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
    print(request.user)
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
def get_projects_list(request):

    users_projects = handle_receipt.get_projects_for_user(request.user)

    context = {"projects": users_projects}

    return render(request, "photo/projects.html", context)
