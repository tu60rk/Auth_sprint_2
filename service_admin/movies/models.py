import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):

    name = models.CharField(verbose_name=_("Genre name"), max_length=255, unique=True)
    description = models.TextField(verbose_name=_("Genre description"), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'content"."genre'
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(verbose_name=_("Name actor"), max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'content"."person'
        verbose_name = "Персона"
        verbose_name_plural = "Персоны"


class FilmWork(UUIDMixin, TimeStampedMixin):
    class Choice(models.TextChoices):
        show = "tv_show", _("TV show")
        movie = "movie", _("Video")

    title = models.CharField(verbose_name=_("Film title"), max_length=255)
    description = models.TextField(verbose_name=_("Film description"), blank=True)
    creation_date = models.DateField(
        verbose_name=_("Date of film creation")
    )
    rating = models.FloatField(
        verbose_name=_("Raiting film"),
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    type = models.CharField(
        verbose_name=_("Film type"), choices=Choice.choices, max_length=100
    )

    file_path = models.FileField(_("file"), blank=True, null=True, upload_to="movies/")

    all_genres = models.ManyToManyField(Genre, through="GenreFilmwork")
    all_persons = models.ManyToManyField(Person, through="PersonFilmwork")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = "Фильмы"
        verbose_name_plural = "Фильмы"

        indexes = [
            models.Index(fields=['creation_date'], name='film_work_creation_date_idx')
        ]


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

        indexes = [
            models.Index(fields=['film_work', 'genre'], name='film_work_genre_idx')
        ]

class Roles(models.TextChoices):
        PRODUCER = 'Producer', _('Producer')
        SCREENWRITER = 'Screenwriter', _('Screenwriter')
        ACTOR = 'Actor', _('Actor')

class PersonFilmwork(UUIDMixin):

    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=255,
        choices=Roles.choices,
        default=Roles.ACTOR,
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = "Персона"
        verbose_name_plural = "Персоны"

        indexes = [
            models.Index(fields=['film_work', 'person', 'role'], name='film_work_person_idx')
        ]


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    verified = models.BooleanField(default=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'

    @property
    def is_staff(self):
        return self.is_active

    # менеджер модели
    objects = MyUserManager()

    def __str__(self):
        return f'{self.email} {self.id}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = 'content"."user'
