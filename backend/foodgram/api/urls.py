from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (IngredientViewSet, RecipeViewSet, TagViewSet,
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
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
