from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

# =================== Сериализатор на ДРФ низкоуровневый ===================
# Сериализаторы работают подобно джанговским формам. Нужно определить, какие поля и как нужно обрабатывать.
# Т.к. именно сериализатор занимается и переводом данных туда-сюда, и сохранением в БД, то здесь нужно определить
# работу методов сохранения и апдейта 

# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
# 
#     def create(self, validated_data):
#         return Snippet.objects.create(**validated_data)
# 
#     def update(self, instance, validated_data):
#         for i_attr in ('title', 'code', 'linenos', 'language', 'style'):
#             setattr(instance, i_attr, validated_data.get(i_attr, getattr(instance, i_attr)))
# 
#         instance.save()
#         return instance


# =================== Сериализаторы на ДРФ высокоуровневые ===================
# ------------------- ModelSerializer -------------------
# Работает подобно ModelForm, т.е. не надо указывать, как именно работать с тем или иным полем, нужно только указать
# модель и те поля, которые надо обрабатывать.
# Но некоторые поля можно и нужно добавлять и прямо указывать, зачем это поле (обязательно потом добавить в общий список
# полей "fields").
# Например, ReadOnlyField(source='owner.username') - позволяет вытащить из связанного "owner" (т.е. Юзер) его имя
# и передать как поле только для чтения.
# PrimaryKeyRelatedField - отображает связи (нужно указать кверисет и много ли связей)
# ВАЖНО: ModelSerializer для отображения отношений использует первичные ключи связанных объектов!
# Т.е. в выходном json мы увидим просто айдишник(и) связей.

# class SnippetSerializer(serializers.ModelSerializer):
#     owner = serializers.ReadOnlyField(source='owner.username')
#
#     class Meta:
#         model = Snippet
#         fields = ['title', 'code', 'highlighted', 'linenos', 'language', 'style', 'owner']


# class UserSerializer(serializers.ModelSerializer):
#     snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
#
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'snippets']


# ------------------- HyperlinkedModelSerializer -------------------
# Он работает как и ModelSerializer, но использует для отображения связей не просто айдишники, а отреверсированные урлы
# Т.е. в выходном json мы увидим готовые адреса для перехода к связанному объекту
# Для ссылки на какую-то вьюху, которая отобразит детальное представление, есть HyperlinkedIdentityField,
# а для ссылок на связанные объекты - HyperlinkedRelatedField

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippets:snippet-highlight', format='html')
    url = serializers.HyperlinkedIdentityField(view_name='snippets:snippet-detail')

    class Meta:
        model = Snippet
        fields = ['url', 'id', 'highlight', 'owner', 'title', 'code', 'linenos', 'language', 'style']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='snippets:user-detail')
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippets:snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets']
