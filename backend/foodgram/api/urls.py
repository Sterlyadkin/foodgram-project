from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (FavoriteViewSet, IngredientViewSet, RecipeViewSet,
                       ShoppingCartViewSet, TagViewSet,
                       UserSubscribeView, UserSubscriptionsViewSet)

router = DefaultRouter()
router.register(r'users/subscriptions', UserSubscriptionsViewSet,
                basename='subscriptions')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'tags', TagViewSet, basename='tags')
router.register(
    r'ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:user_id>/subscribe/', UserSubscribeView.as_view()),
    path('recipes/<recipes_id>/favorite/',
         FavoriteViewSet.as_view({'post': 'post',
                                  'delete': 'delete'})),
    path('recipes/<recipes_id>/shopping_cart/',
         ShoppingCartViewSet.as_view({'post': 'post',
                                     'delete': 'delete'})),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
