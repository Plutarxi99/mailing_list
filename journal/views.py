from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.template.base import logger
from django.urls import reverse_lazy, reverse

from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from journal.forms import JournalForm
from journal.models import Journal

from django.core.mail import send_mail


class JournalCreateView(CreateView):
    model = Journal
    form_class = JournalForm
    success_url = reverse_lazy('journal:list')

    def form_valid(self, form):
        if form.is_valid:
            new_journal = form.save()
            new_journal.slug = slugify(new_journal.title)
            new_journal.save()

        return super().form_valid(form)


class JournalUpdateView(PermissionRequiredMixin, UpdateView):
    model = Journal
    form_class = JournalForm
    permission_required = 'journal.change_journal'

    def form_valid(self, form):
        if form.is_valid:
            new_journal = form.save()
            new_journal.slug = slugify(new_journal.title)
            new_journal.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('journal:view', args=[self.kwargs.get('pk')])


class JournalListView(ListView):
    model = Journal

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not self.request.user.groups.filter(name='Manager').exists() or self.request.user.is_superuser:
            queryset = queryset.filter(published_is=False)
        return queryset


class JournalDetailView(DetailView):
    model = Journal

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_view += 1
        self.object.save()
        return self.object


class JournalDeleteView(PermissionRequiredMixin, DeleteView):
    model = Journal
    success_url = reverse_lazy('journal:list')
    permission_required = 'journal.delete_journal'


def is_publish(request, pk):
    journal_item = get_object_or_404(Journal, pk=pk)
    if journal_item.published_is:
        journal_item.published_is = False
    else:
        journal_item.published_is = True
    journal_item.save()

    return redirect(reverse('journal:list'))
