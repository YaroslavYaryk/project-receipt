from django import forms
from .models import Receipt, Project
import datetime


class ReceiptForm(forms.ModelForm):

    date = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M"],
        widget=forms.DateTimeInput(
            attrs={
                "class": "form-control datetimepicker-input",
                "data-target": "#datetimepicker1",
                "initial": datetime.date.today,
            }
        ),
    )

    class Meta:
        model = Receipt
        fields = (
            "date",
            "price",
            "comment",
            "company",
            "description",
            "business",
            "persons",
        )

        widgets = {
            "comment": forms.Textarea(attrs={"rows": 2, "cols": 15}),
            "description": forms.Textarea(attrs={"rows": 2, "cols": 15}),
        }

    def __init__(self, *args, **kwargs):
        super(ReceiptForm, self).__init__(*args, **kwargs)
        self.fields["date"].initial = datetime.date.today


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("name",)
