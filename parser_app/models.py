# parser_app/models.py
from django.db import models
from django.contrib.postgres.fields import ArrayField

class Doctor(models.Model):
    kv_id = models.BigIntegerField(unique=True, help_text="Hashed unique ID")
    title = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    street = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    fax = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    languages = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    specializations = ArrayField(models.CharField(max_length=500), blank=True, null=True)
    opening_hours = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"
        ordering = ['name']