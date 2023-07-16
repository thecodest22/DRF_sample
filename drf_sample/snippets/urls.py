from django.urls import path, include
from rest_framework import renderers
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    # api_root,
    # SnippetList,
    # SnippetDetail,
    # UserList,
    # UserDetail,
    # SnippetHighlight,
    SnippetViewSet,
    UserViewSet,
)


app_name = 'snippets'

# urlpatterns = [
#     path('', api_root),
#
#     path('snippets/', SnippetList.as_view(), name='snippet_list'),
#     path('snippets/<int:pk>/', SnippetDetail.as_view(), name='snippet_detail'),
#     path('snippets/<int:pk>/highlight/', SnippetHighlight.as_view(), name='snippet_highlight'),
#
#     path('users/', UserList.as_view(), name='user_list'),
#     path('users/<int:pk>/', UserDetail.as_view(), name='user_detail'),
# ]
# urlpatterns = format_suffix_patterns(urlpatterns)



# =================== Для использования вьюсетов ===================
# -------- Можно явно сопоставить методы вьюсетов с типами запросов и связать с конкретными представлениями --------

# snippet_list = SnippetViewSet.as_view({
#     'get': 'list',
#     'post': 'create',
# })
#
# snippet_detail = SnippetViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy',
# })
#
# snippet_highlight = SnippetViewSet.as_view({
#     'get': 'highlight',
# }, renderer_classes=[renderers.StaticHTMLRenderer])
#
# user_list = UserViewSet.as_view({
#     'get': 'list',
# })
#
# user_detail = UserViewSet.as_view({
#     'get': 'retrieve',
# })
#
# urlpatterns = [
#     path('', api_root),
#
#     path('snippets/', snippet_list, name='snippet_list'),
#     path('snippets/<int:pk>/', snippet_detail, name='snippet_detail'),
#     path('snippets/<int:pk>/highlight/', snippet_highlight, name='snippet_highlight'),
#
#     path('users/', user_list, name='user_list'),
#     path('users/<int:pk>/', user_detail, name='user_detail'),
# ]
# urlpatterns = format_suffix_patterns(urlpatterns)

# -------- А можно использовать коробочную маршрутизацию --------
# Встроенный инструмент сам раскидает маршруты, нужно только передать ему строку-путь и нужный вьюсет.
# Корневой ендпоинт, который писали сами, больше не нужен. Также он добавляет суффиксы
router = DefaultRouter()
router.register('snippets', SnippetViewSet, basename='snippet')
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
