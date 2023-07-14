from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import snippet_list, snippet_detail


app_name = 'snippets'

urlpatterns = [
    path('snippets/', snippet_list, name='snippet_list'),
    path('snippets/<int:pk>/', snippet_detail, name='snippet_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
