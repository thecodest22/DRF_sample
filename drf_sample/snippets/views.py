from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, mixins, generics, permissions, renderers, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .models import Snippet
from .serializers import SnippetSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly


# =================== Вьюхи на чистом Джанго ===================
# Здесь используются сериализаторы ДРФ, но ответ возвращается в виде обычного JSONResponse.
# Методы обработки запросов пишутся вручную, парсинг указывается вручную. Парсим реквест и передаем данные сериализатору

# @csrf_exempt
# def snippet_list(request):
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     if request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(data=data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#
#         return JsonResponse(serializer.errors, status=400)


# @csrf_exempt
# def snippet_detail(request, pk):
#     snippet = get_object_or_404(Snippet, pk=pk)
#
#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return JsonResponse(serializer.data)
#     if request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(snippet, data=data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#
#         return JsonResponse(serializer.errors, status=400)
#
#     if request.method == 'DELETE':
#         snippet.delete()
#         return HttpResponse(status=204)


# =================== Вьюхи на ДРФ как функции ===================
# Оборачиваем декораторами, ограничивающими возможные типы запросов. Также используем format (нужно добавить в урлах
# приложения), чтобы можно было обращаться к ендпоинтам с суффиксами (".json", ".html" и т.д.).
# Также юзаем ДРФовский Response, т.к. ему удобнее передавать именованные статусы

# @api_view(['GET', 'POST'])
# def snippet_list(request, format=None):
#
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     if request.method == 'POST':
#         serializer = SnippetSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk, format=None):
#     snippet = get_object_or_404(Snippet, pk=pk)
#
#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     if request.method == 'PUT':
#         serializer = SnippetSerializer(snippet, data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# =================== Вьюхи на ДРФ низкоуровневые ===================
# Используется ДРФ APIView. Он так же требует настроить обработку разных типов запросов

# class SnippetList(APIView):
#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SnippetDetail(APIView):
#     def get(self, request, pk, format=None):
#         snippet = get_object_or_404(Snippet, pk=pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, pk, format=None):
#         snippet = get_object_or_404(Snippet, pk=pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         snippet = get_object_or_404(Snippet, pk=pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# =================== Вьюхи на ДРФ среднеуровневые ===================
# Применяем GenericAPIView, а также миксины, которые содержат нужный функционал для CRUD.
# Нужно только на уровне класса определить кверисет и класс сериализатора, а также в соответствии с типом запроса
# вернуть нужные функции миксинов

# class SnippetsList(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
#                    generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# class SnippetDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# =================== Вьюхи на ДРФ высокоуровневые ===================
# Применяем дженерик-вью разной степени смешения. Например, ListCreateAPIView позволяет отобразить список и сразу
# добавляет форму для создания. Также здесь вешаем нужные разрешения - как встроенные, так и самописные.
# Для минимального функционала нужно указать кверисет и класс сериализатора.

# class SnippetList(generics.ListCreateAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Сниппет связан с Юзером. И нужно, чтобы при создании через форму создавалась связь с автором, т.е. Юзером.
    # Поэтому надо переопределить метод сохранения (он в CreateModelMixin) и передать в метод сохранения сериализатора
    # дополнительные данные. Берем Юзера из реквеста и передаем его как значение для "owner".
    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# class SnippetHighlight(generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     renderer_classes = [renderers.StaticHTMLRenderer]
#
#     def get(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)


# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# Это "корневой эндпоинт". Он возвращает ДРФ-респонс в виде словаря. Ключи - удобные нам слова, значения - результат
# ДРФ-реверса. Ему передаем имя нужного вью. Почему-то не хочет работать, если не указать пространство имен приложения
# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'users': reverse('snippets:user_list', request=request, format=format),
#         'snippets': reverse('snippets:snippet_list', request=request, format=format)
#     }, status=status.HTTP_200_OK)


# =================== Вьюсеты ===================
# Функционал нескольких вьюх можно объединить во ViewSet.
# Например, можно объединить UserList и UserDetail в ReadOnlyModelViewSet. Он сразу предоставит возможности
# list и retrieve. Останется определить только кверисет и класс сериализатора.


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Также можно объединить SnippetList, SnippetDetail и SnippetHighlight в один ModelViewSet. Он дает все CRUD.
# Но нужно прописать разрешения, иначе CRUD будет доступен для всех.
# Если же стандартного CRUD недостаточно, то есть нужны какие-то особые отображения или сохранения, то их можно дописать
class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # Так помечаются кастомные действия, которые будут сопоставлены с каким-либо из типов запроса.
    # Например, GET-запрос по урлу, который ведет к highlight, будет обрабатываться функцией "highlight" (см. урлы!)
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
