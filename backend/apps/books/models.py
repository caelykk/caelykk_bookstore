from django.db import models

# Create your models here.
class Book(models.Model):
	from django.db import models
from django.utils.text import slugify

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug", help_text="URL-friendly версия названия")
    description = models.TextField(blank=True, verbose_name="Описание")
    edition = models.CharField(
        max_length=50,
        verbose_name="Издание",
        help_text="Например, '1-е', '2-е' и т.д."
    )
    volume = models.PositiveIntegerField(
        verbose_name="Том",
        null=True,
        blank=True,
        help_text="Номер тома, если книга состоит из нескольких томов"
    )
    print_run = models.PositiveIntegerField(
        verbose_name="Тираж",
        null=True,
        blank=True,
        help_text="Количество напечатанных экземпляров"
    )
    publication_date = models.DateField(
        verbose_name="Дата публикации",
        null=True,
        blank=True
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Цена"
    )
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Скидка",
        null=True,
        blank=True,
        help_text="Процент скидки, например, 10.00 для 10%"
    )
    stock = models.PositiveIntegerField(
        verbose_name="Количество на складе",
        default=0
    )
    available = models.BooleanField(
        default=True,
        verbose_name="Доступность"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания записи"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления записи"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Автоматическая генерация slug из названия, если он не задан
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def get_discounted_price(self):
	    if self.discount:
	        return self.price - (self.price * self.discount / 100)
	    return self.price