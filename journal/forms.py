from django import forms

from journal.models import Journal


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class JournalForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Journal
        exclude = ('slug', 'count_view', 'published_is',)
