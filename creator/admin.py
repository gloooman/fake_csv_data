from django.contrib import admin
from creator.models import Schema, Column, DataSet


@admin.register(Schema)
class SchemaAdmin(admin.ModelAdmin):
    pass


@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    pass


@admin.register(DataSet)
class DataSetAdmin(admin.ModelAdmin):
    pass
