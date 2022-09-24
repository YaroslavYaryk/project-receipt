from photoproject.models import Category, Photo, Project, Receipt
from django.utils.text import slugify


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
    return Category.objects.create(name=name, slug=slugify(name))


def handle_create_project(name, user):
    return Project.objects.create(name=name, user=user)


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
