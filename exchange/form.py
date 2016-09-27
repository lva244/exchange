from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from django.core.validators import RegexValidator

from .models import RegisterLike

class RegisterLikeForm(forms.ModelForm):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    access_token = forms.CharField(
        label="Access Token",
        validators=[alphanumeric],
        required=True
    )

    post_id = forms.CharField(
        label="Post ID",
        validators=[alphanumeric],
        required=True
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-7'

        self.helper.layout = Layout(
            Field('access_token'),
            Field('post_id')
        )

        self.helper.add_input(Submit('submit', 'Submit', css_class="btn-primary"))
        super(RegisterLikeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = RegisterLike
        fields = ['access_token']


class ImportForm(forms.Form):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    list_token = forms.CharField(
        label='Token List',
        required=True,
        widget=forms.Textarea(),
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-7'

        self.helper.layout = Layout(
            Field('list_token')
        )

        self.helper.add_input(Submit('submit', 'Submit', css_class="btn-primary"))
        super(ImportForm, self).__init__(*args, **kwargs)

    class Meta:
        pass
