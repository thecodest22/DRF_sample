from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    # snippet_list,
    # snippet_detail,
    SnippetList,
    SnippetDetail,
    UserList,
    UserDetail,
    api_root,
    SnippetHighlight
)


app_name = 'snippets'

urlpatterns = [
    # path('snippets/', snippet_list, name='snippet_list'),
    # path('snippets/<int:pk>/', snippet_detail, name='snippet_detail'),
    path('', api_root),
    path('snippets/', SnippetList.as_view(), name='snippet_list'),
    path('snippets/<int:pk>/highlight/', SnippetHighlight.as_view(), name='snippet_highlight'),
    path('users/', UserList.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
