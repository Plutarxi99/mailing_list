from django import forms

from journal.models import Journal


class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = '__all__'
        exclude = ('slug', 'count_view', )