from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields["username"], "Your username")
        add_placeholder(self.fields["email"], "Your e-mail")
        add_placeholder(self.fields["first_name"], "Ex.: John")
        add_placeholder(self.fields["last_name"], "Ex.: Doe")
        add_placeholder(self.fields["password"], "Type your password")
        add_placeholder(self.fields["password2"], "Repeat your password")

    username = forms.CharField(
        label="Username",
        help_text=(
            "Username must have letters, numbers or one of those @.+-_. "
            "The length should be between 4 and 150 characters."
        ),
        error_messages={
            "required": "This field must not be empty",
            "min_length": "Username must have at least 4 characters.",
            "max_length": "Username must have less than 150 characters.",
        },
        min_length=4,
        max_length=150,
    )
    first_name = forms.CharField(
        error_messages={"required": "Write your first name"},
        label="First name",
    )
    last_name = forms.CharField(
        error_messages={"required": "Write your last name"},
        label="Last name",
    )
    email = forms.EmailField(
        error_messages={"required": "E-mail is required"},
        label="E-mail",
        help_text="The e-mail must be valid.",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={"required": "Password must not be empty"},
        help_text=(
            "Password must have at least one uppercase letter, "
            "one lowercase letter and one number. The length should be "
            "at least 8 characters."
        ),
        validators=[strong_password],
        label="Password",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label="Password2",
        error_messages={"required": "Please, repeat your password"},
    )

    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]

    def clean_email(self):  # sourcery skip: use-named-expression
        email = self.cleaned_data.get("email", "")
        exists = get_user_model().objects.filter(email=email).exists()
        if exists:
            raise ValidationError(
                "User e-mail is already in use",
                code="invalid",
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            password_confirmation_error = ValidationError(
                "Password and password2 must be equal",
                code="invalid",
            )

            raise ValidationError(
                {
                    "password": password_confirmation_error,
                    "password2": [
                        password_confirmation_error,
                    ],
                }
            )


# import re

# from django import forms
# from django.contrib.auth import get_user_model
# from django.core.exceptions import ValidationError


# def add_attr(field, attr_name, attr_new_val):
#     existing = field.widget.attrs.get(attr_name, "")
#     field.widget.attrs[attr_name] = f"{existing} {attr_new_val}".strip()


# def add_placeholder(field, placeholder_val):
#     add_attr(field, "placeholder", placeholder_val)


# def strong_password(password):
#     regex = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$")

#     if not regex.match(password):
#         raise ValidationError(
#             "Password must have at least one uppercase letter, "
#             "one lowercase letter and one number. The length should be "
#             "at least 8 characters.",
#             code="invalid_password",
#         )


# class RegisterForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         add_placeholder(self.fields["username"], "Your username")
#         add_placeholder(self.fields["email"], "Your e-mail")
#         add_placeholder(self.fields["first_name"], "Ex.: John")
#         add_placeholder(self.fields["last_name"], "Ex.: Doe")
#         add_attr(self.fields["username"], "css", "a-css-class")

#     password = forms.CharField(
#         required=True,
#         widget=forms.PasswordInput(attrs={"placeholder": "Your password"}),
#         error_messages={"required": "Password must not be empty"},
#         help_text=(
#             "Password must have at least one uppercase letter, "
#             "one lowercase letter and one number. The length should be "
#             "at least 8 characters."
#         ),
#         validators=[strong_password],
#     )
#     password2 = forms.CharField(
#         required=True,
#         widget=forms.PasswordInput(
#             attrs={"placeholder": "Repeat your password"}
#         ),
#     )

#     class Meta:
#         model = get_user_model()
#         fields = [
#             "first_name",
#             "last_name",
#             "username",
#             "email",
#             "password",
#         ]
#         # exclude = ['first_name']
#         labels = {
#             "username": "Username",
#             "first_name": "First name",
#             "last_name": "Last name",
#             "email": "E-mail",
#             "password": "Password",
#         }
#         help_texts = {
#             "email": "The e-mail must be valid.",
#         }
#         error_messages = {
#             "username": {
#                 "required": "This field must not be empty",
#             }
#         }
#         widgets = {
#             "first_name": forms.TextInput(
#                 attrs={
#                     "placeholder": "Type your username here",
#                     "class": "input text-input",
#                 }
#             ),
#             "password": forms.PasswordInput(
#                 attrs={"placeholder": "Type your password here"}
#             ),
#         }

#     def clean_password(self):
#         data = self.cleaned_data.get("password")

#         if "atenção" in data:
#             raise ValidationError(
#                 "Não digite %(value)s no campo password",
#                 code="invalid",
#                 params={"value": "atenção"},
#             )

#         return data

#     def clean_first_name(self):
#         data = self.cleaned_data.get("first_name")

#         if "John Doe" in data:
#             raise ValidationError(
#                 "Não digite %(value)s no campo first name",
#                 code="invalid",
#                 params={"value": "John Doe"},
#             )

#         return data

#     def clean(self):
#         cleaned_data = super().clean()

#         password = cleaned_data.get("password")
#         password2 = cleaned_data.get("password2")

#         if password != password2:
#             password_confirmation_error = ValidationError(
#                 "Password and password2 must be equal",
#                 code="invalid",
#             )

#             raise ValidationError(
#                 {
#                     "password": password_confirmation_error,
#                     "password2": [
#                         password_confirmation_error,
#                     ],
#                 }
#             )
