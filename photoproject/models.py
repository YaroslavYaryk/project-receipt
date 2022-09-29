from django.db import models
from django.utils import timezone
from accounts.models import User

# Create your models here.
class Category(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL", null=True
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Photo(models.Model):

    photo = models.ImageField(upload_to="photo/Data%y/%m/%d/", null=True, blank=True)

    def __str__(self):
        return self.photo.url


class Project(models.Model):

    name = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Receipt(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)

    photos = models.ManyToManyField(Photo)

    company = models.CharField(max_length=150, null=True)

    date = models.DateField(default=timezone.now)

    price = models.FloatField()

    description = models.TextField(blank=True)

    business = models.CharField(max_length=150, null=True)

    persons = models.CharField(max_length=100, null=True)

    comment = models.TextField(blank=True)

    file_document = models.FileField(
        upload_to="exel/Data%y/%m/%d/", max_length=100, null=True
    )

    def __str__(self):
        return f"{self.category.name} - {self.user.name} - {self.date} - {self.price}"


class ProjectReceipts(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    file_document = models.FileField(
        upload_to="exel/Data%y/%m/%d/", max_length=100, null=True
    )

    date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f"{self.project} - {self.date}"
