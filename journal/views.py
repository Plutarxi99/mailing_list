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


class JournalUpdateView(UpdateView):
    model = Journal
    form_class = JournalForm

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

    # def get_queryset(self, *args, **kwargs):
    #     queryset = super().get_queryset(*args, **kwargs)
    #     queryset = queryset.filter(published_is=False)
    #     return queryset


class JournalDetailView(DetailView):
    model = Journal

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_view += 1
        self.object.save()
        if self.object.count_view == 100:
            pass
            # send_mail_about_100_views(self.object.id)
        return self.object


class JournalDeleteView(DeleteView):
    model = Journal
    success_url = reverse_lazy('journal:list')


def is_publish(request, pk):
    journal_item = get_object_or_404(Journal, pk=pk)
    if journal_item.published_is:
        journal_item.published_is = False
    else:
        journal_item.published_is = True
    journal_item.save()

    return redirect(reverse('journal:list'))
#
#
# def send_mail_about_100_views(journal_id: int):
#     journal = Journal.objects.get(pk=journal_id)
#     if journal.count_view != 100:
#         logger.error(
#             'Функция вызвана для статьи %d, к которой %d просмотров',
#             journal.pk, journal.count_view
#         )
#     return send_mail(subject='Популярная статья',
#                      message=f'Статья {journal.title} была просмотрена 100 раз',
#                      from_email="shievanov.egor@yandex.ru",
#                      recipient_list=["egor.shievanov@gmail.com"],
#                      fail_silently=False,
#                      )
