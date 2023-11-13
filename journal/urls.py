from django.urls import path
from journal.apps import JournalConfig
from journal.views import JournalCreateView, JournalListView, JournalDetailView, JournalUpdateView, JournalDeleteView, \
    is_publish

app_name = JournalConfig.name


urlpatterns = [
    path('create/', JournalCreateView.as_view(), name='create'),
    path('', JournalListView.as_view(), name='list'),
    path('view/<int:pk>/', JournalDetailView.as_view(), name='view'),
    path('edit/<int:pk>/', JournalUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', JournalDeleteView.as_view(), name='delete'),
    path('publish/<int:pk>/', is_publish, name='published_is'),
    # path('count_view/<int:pk>/', send_email, name='count_view'),
    # path('count_view/<int:pk>/', send_email, name='count_view'),
]