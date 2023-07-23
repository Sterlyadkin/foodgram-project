from django.db.models import Exists, OuterRef
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,)
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (IngredientSerializer,
                             RecipeCreateSerializer,
                             RecipeReadSerializer, RecipeSerializer,
                             TagSerializer,
                             SubscriptionsSerializer,
                             SubscribeAuthorSerializer)
from api.utils import get_shopping_cart
from recipes.models import (Favorite, Ingredient, Recipe,
                            ShoppingCart, Tag)
from users.models import Subscription, User


class UserSubscribeView(APIView):
    """Создание/удаление подписки на пользователя."""
    def post(self, request, user_id):
        author = get_object_or_404(User, id=user_id)
        serializer = SubscribeAuthorSerializer(
            data={'user': request.user.id, 'author': author.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        author = get_object_or_404(User, id=user_id)
        if not Subscription.objects.filter(user=request.user,
                                           author=author
                                           ).delete()[0]:
            raise Response(
                {'errors': 'Вы не подписаны на этого пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserSubscriptionsViewSet(mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    """Получение списка всех подписок на пользователей."""
    serializer_class = SubscriptionsSerializer

    def get_queryset(self):
        return User.objects.filter(
            following__user=self.request.user)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter
    http_method_names = ['get', 'post', 'patch', 'create', 'delete']

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return self.queryset.order_by('-id')
        return self.queryset.annotate(
            is_favorited=Exists(Favorite.objects.filter(
                recipe__pk=OuterRef('pk'),
                user=user
            )),
            is_in_shopping_cart=Exists(ShoppingCart.objects.filter(
                recipe__pk=OuterRef('pk'),
                user=user
            ))
        ).order_by('-id')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeCreateSerializer

    @action(detail=False, methods=['get'],
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        """Отправка файла со списком покупок."""
        shopping_list = get_shopping_cart(self.request.user)
        response = FileResponse(shopping_list, content_type='text/plain')
        response[
            'Content-Disposition'] = 'attachment; filename="shopping_cart.txt"'
        return response

    @action(detail=True, methods=['post', 'delete'], name='favorite')
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_obj(Favorite, request, pk)
        return self.del_obj(Favorite, request, pk)

    @action(detail=True, methods=['post', 'delete'], name='shopping_cart')
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_obj(ShoppingCart, request, pk)
        return self.del_obj(ShoppingCart, request, pk)

    def add_obj(self, model, request, pk):
        if not model.objects.filter(user=request.user, recipe=pk).exists():
            obj = model.objects.create(
                user=request.user,
                recipe=get_object_or_404(Recipe, id=pk)
            )
            serializer = RecipeSerializer(obj.recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def del_obj(self, model, request, pk):
        model.objects.filter(
            user=request.user,
            recipe=pk
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
