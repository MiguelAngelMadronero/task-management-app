from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, HTML
from core.models import Project, Task

# from api import models


class LoginForm(forms.Form):
    """Login password."""

    email = forms.CharField(label=("Email"), max_length=255, required=True)
    password = forms.CharField(
        label=("Password"), widget=forms.PasswordInput, required=True)
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        """Init."""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(
            Submit('submit', ('Submit'), css_class='btn-primary'))
        self.helper.form_method = 'POST'

    def clean(self):
        """Clean."""
        email = self.cleaned_data.get('email', '').lower()
        password = self.cleaned_data.get('password')
        user = None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError(
                ('Email or password incorrect, please try again.'))
        if user.is_active is False:
            raise forms.ValidationError(('Your account is not active.'))
        user = authenticate(username=user.username, password=password)
        if not user:
            raise forms.ValidationError(
                ('Email or password incorrect, please try again.'))
        return self.cleaned_data

    def login(self):
        """Login method."""
        email = self.cleaned_data.get('email', '').lower()
        password = self.cleaned_data.get('password')
        username = User.objects.get(email=email).username
        user = authenticate(username=username, password=password)
        return user


class SignUpForm(forms.ModelForm):
    """SignUp Form."""

    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['email'].required = True
        self.fields['password'].required = True
        for field in self.fields.values():
            field.widget.attrs['autocomplete'] = 'off'
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'email',
            'password',
            HTML("""
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary"
                     data-bs-dismiss="modal">{{ _("Close") }}</button>
                    <button type="submit" class="btn btn-primary">
                    {{ _("Save changes") }}</button>
                </div>
            """)
        )

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

    def clean(self):
        """Check the form."""
        cleaned_data = super().clean()
        email = cleaned_data.get('email', '').lower()
        if User.objects.filter(
                email=email).exclude(pk=self.instance.pk).exists():
            self.add_error('email', (
                'A user with this email already exists.'))
        return cleaned_data

    class Meta(object):
        """Meta class."""

        model = User
        fields = ('username', 'email', 'password')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        for field in self.fields.values():
            field.widget.attrs['autocomplete'] = 'off'
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'description',
        )
        self.helper = FormHelper()
        self.helper.add_input(
            Submit('submit', ('Submit'), css_class='btn-primary'))
        self.helper.form_method = 'POST'


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status', 'assigned_to']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True
        for field in self.fields.values():
            field.widget.attrs['autocomplete'] = 'off'
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'description',
            'due_date',
            'status',
            'assigned_to',
        )
        self.helper = FormHelper()
        self.helper.add_input(
            Submit('submit', ('Submit'), css_class='btn-primary'))
        self.helper.form_method = 'POST'


# class UsersForm(forms.ModelForm):
#     """Users Form."""

#     required_css_class = 'required'
#     phone_1 = forms.CharField(required=False, max_length=20)
#     address = forms.CharField(required=False, max_length=200)
#     identification_type = forms.ChoiceField(
#         required=True, choices=models.UserProfile.IdentificationType.choices)
#     identification_number = forms.CharField(required=True, max_length=200)
#     contract = forms.CharField(required=False)

#     def __init__(self, *args, **kwargs):
#         super(UsersForm, self).__init__(*args, **kwargs)
#         self.fields['email'].required = True
#         self.fields['first_name'].required = True
#         self.fields['last_name'].required = True
#         for field in self.fields.values():
#             field.widget.attrs['autocomplete'] = 'off'
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             'email',
#             'first_name',
#             'last_name',
#             HTML("""
#                 <div class="modal-footer">
#                     <button type="button" class="btn btn-secondary"
#                      data-bs-dismiss="modal">{{ _("Close") }}</button>
#                     <button type="submit" class="btn btn-primary">
#                     {{ _("Save changes") }}</button>
#                 </div>
#             """)
#         )

#     def save(self, commit=True):
#         user = super(UsersForm, self).save(commit=False)
#         user.username = self.cleaned_data['email']
#         user.set_password(self.cleaned_data['identification_number'])
#         user.save()
#         user_profile = models.UserProfile(
#             user=user,
#             phone_1=self.cleaned_data['phone_1'],
#             address=self.cleaned_data['address'],
#             identification_type=self.cleaned_data['identification_type'],
#             identification_number=self.cleaned_data['identification_number'],
#             contract=self.cleaned_data['contract'],
#             is_active=self.cleaned_data['is_active'],
#         )
#         user_profile.save()
#         return user

#     def clean(self):
#         """Check the form."""
#         cleaned_data = super().clean()
#         email = cleaned_data.get('email', '').lower()
#         if models.User.objects.filter(
#                 email=email).exclude(pk=self.instance.pk).exists():
#             self.add_error('email', (
#                 'A user with this email already exists.'))
#         return cleaned_data
