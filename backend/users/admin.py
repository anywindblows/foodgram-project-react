from config import config_messages as msg
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from .models import Follow, User


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
        help_text=msg.CHANGE_PASSWORD
    )

    class Meta:
        model = User
        fields = ('username',)

    def clean_password(self):
        return self.initial['password']


class UserModelAdmin(BaseUserAdmin):
    """
    User admin panel.
    With custom filter params.
    """
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'username')
    list_filter = ('is_superuser', 'is_staff', 'is_active')
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
    ordering = ('-username',)
    filter_horizontal = ()


class FollowModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'author']
    list_filter = ['user', 'author']


admin.site.register(Follow, FollowModelAdmin)
admin.site.register(User, UserModelAdmin)
admin.site.unregister(Group)
