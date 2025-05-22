from collections import defaultdict

from django import forms
from django.forms import ValidationError

from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields["preparation_steps"], "class", "span-2")

    class Meta:
        model = Recipe
        fields = (
            "title",
            "description",
            "preparation_time",
            "preparation_time_unit",
            "servings",
            "servings_unit",
            "preparation_steps",
            "cover",
        )
        widgets = {
            "cover": forms.FileInput(attrs={"class": "span-2"}),
            "servings_unit": forms.Select(
                choices=(
                    ("Porções", "Porções"),
                    ("Pedaçoes", "Pedaçoes"),
                    ("Pessoas", "Pessoas"),
                )
            ),
            "preparation_time_unit": forms.Select(
                choices=(
                    ("Minutos", "Minutos"),
                    ("Horas", "Horas"),
                )
            ),
        }

    def clean(self, *args, **kwargs):
        # sourcery skip: inline-immediately-returned-variable
        super_clean = super().clean(*args, **kwargs)
        cleaned_data = self.cleaned_data
        title = cleaned_data.get("title")
        description = cleaned_data.get("description")

        if title == description:
            self._my_errors["title"].append("Cannot be equal to description.")
            self._my_errors["description"].append("Cannot be equal to title.")

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get("title")
        title_char_number = 5

        if len(title) < title_char_number:
            self._my_errors["title"].append("Must have at least 5 chars.")

        return title

    def clean_preparation_time(self):  # sourcery skip: class-extract-method
        field_name = "preparation_time"
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(field_value):
            self._my_errors["preparation_time"].append(
                "Must be a positive number"
            )

        return field_value

    def clean_servings(self):
        field_name = "servings"
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(field_value):
            self._my_errors["servings"].append("Must be a positive number")

        return field_value
