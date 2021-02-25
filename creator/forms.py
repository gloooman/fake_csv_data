from django.forms import ModelForm, inlineformset_factory

from creator.models import Schema, Column


class ColumnForm(ModelForm):
    class Meta:
        model = Column
        exclude = ()


ColumnFormSet = inlineformset_factory(
    Schema, Column, form=ColumnForm, extra=1)
