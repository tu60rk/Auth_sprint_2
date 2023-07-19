from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Genre, FilmWork, GenreFilmwork, Person, PersonFilmwork
from movies.models import User


class DecadeRatingFilter(admin.SimpleListFilter):

    title = _("decade rating")
    parameter_name = "rating"

    def lookups(self, request, model_admin):
        return (
            ("0 - 25", _("between 0 and 25")),
            ("25 - 50", _("between 25 and 50")),
            ("50 - 75", _("between 50 and 75")),
            ("75 - 100", _("between 75 and 100")),
        )

    def queryset(self, request, queryset):

        if self.value() == "0 - 25":
            return queryset.filter(rating__gte=0, rating__lte=25)
        elif self.value() == "25 - 50":
            return queryset.filter(rating__gte=25, rating__lte=50)

        elif self.value() == "50 - 75":
            return queryset.filter(rating__gte=50, rating__lte=75)

        elif self.value() == "75 - 100":
            return queryset.filter(rating__gte=75, rating__lte=100)
        else:
            return queryset


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "description",
    )
    list_filter = ("name",)

    search_fields = ("name", "description", "created", "id")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):

    list_display = ("full_name",)
    search_fields = ("full_name", "created", "id")


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    autocomplete_fields = ("genre",)


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ("person",)


@admin.register(FilmWork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (
        GenreFilmworkInline,
        PersonFilmworkInline,
    )

    list_display = (
        "title",
        "type",
        "creation_date",
        "rating",
    )
    list_filter = ("type", "creation_date", DecadeRatingFilter)
    search_fields = ("title", "description", "created", "id")


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["email"]
        # fields = ["email", "date_of_birth"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        # fields = ["email", "password", "date_of_birth", "is_active", "is_admin"]
        fields = ["email", "password", "is_active"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    # list_display = ["email", "date_of_birth", "is_admin"]
    list_display = ["email"]
    list_filter = ["is_active"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        # ("Personal info", {"fields": ["date_of_birth"]}),
        # ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email"]
                #"fields": ["email", "date_of_birth", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
