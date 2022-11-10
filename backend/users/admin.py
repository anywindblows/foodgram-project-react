from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from .models import User


class UserCreationForm(forms.ModelForm):
    """Form for creating a new user using admin panel."""
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        """Password validation."""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """Save password."""
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """Form for change user password using admin panel."""
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text=(
            "Raw passwords are not stored, so there is no way to see "
            "this user's password, but you can change the password "
            "using <a href=\"../password/\">this form</a>."
        )
    )

    class Meta:
        model = User
        fields = ('username',)

    def clean_password(self):
        return self.initial['password']


class UserAdmin(BaseUserAdmin):
    """
    User admin panel.
    With custom filter params.
    """
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'username')
    list_filter = ('email', 'username')
    fieldsets = (('Personal info', {
        'fields': ('email', 'username', 'first_name', 'last_name',
                   'password', 'is_superuser', 'is_staff', 'is_active')
    }),)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name',
                       'last_name', 'password1', 'password2',
                       'is_superuser', 'is_staff', 'is_active')
        }),)
    search_fields = ('email', 'username')
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
