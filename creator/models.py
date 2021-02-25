import random

from django.contrib.auth.models import User
from django.db import models


def schema_directory_path(instance: 'DataSets', filename):
    return 'schema_{0}/{1}'.format(instance.schema.id, filename)


class Schema(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField('Title', max_length=64)
    created = models.DateField('Created', auto_now_add=True)
    modified = models.DateField('Modified', auto_now=True)

    def __str__(self):
        return f"Schema: {self.name}"


class Column(models.Model):

    class Type(models.TextChoices):
        EMAIL = 'email'
        FULL_NAME = 'full_name'
        JOB = 'job'
        COMPANY_NAME = 'company_name'
        INTEGER = 'integer'
        ADDRESS = 'address'
        DATE = 'date'

    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    col_name = models.CharField('Column name', max_length=64)
    col_type = models.CharField('Type', max_length=16, choices=Type.choices)
    range_from = models.IntegerField('Range From', default=0, blank=True, null=True)
    range_to = models.IntegerField('Range To', default=10, blank=True, null=True)
    order = models.IntegerField('Order', default=0)

    def __str__(self):
        return f"{self.schema}; Column name: {self.col_name}"

    def get_fake_data(self, fake):
        if self.col_type == Column.Type.EMAIL:
            return fake.ascii_email()
        elif self.col_type == Column.Type.ADDRESS:
            return fake.address()
        elif self.col_type == Column.Type.FULL_NAME:
            return fake.name()
        elif self.col_type == Column.Type.JOB:
            return fake.job()
        elif self.col_type == Column.Type.COMPANY_NAME:
            return fake.company()
        elif self.col_type == Column.Type.INTEGER:
            if self.range_to and self.range_from:
                return random.randint(self.range_from, self.range_to)
            else:
                return random.randint(0, 10)
        elif self.col_type == Column.Type.DATE:
            return fake.date()


class DataSet(models.Model):

    class Status(models.TextChoices):
        READY = 'ready'
        PROCESSING = 'processing'
        ERROR = 'error'

    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    path = models.FileField('File path', upload_to=schema_directory_path, blank=True)
    status = models.CharField('Status', max_length=16, choices=Status.choices, default=Status.PROCESSING)
    rows = models.IntegerField('Rows', default=50)
    created = models.DateField('Created', auto_now_add=True)
    modified = models.DateField('Modified', auto_now=True)

    def __str__(self):
        return f"{self.schema}; Created: {self.created}, {self.status}"

    @property
    def image_url(self):
        if self.path and hasattr(self.path, 'url'):
            return self.path.url

