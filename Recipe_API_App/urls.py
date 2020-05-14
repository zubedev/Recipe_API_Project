"""Recipe API App - urls.py"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from Recipe_API_App import views

router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
router.register('recipes', views.RecipeViewSet)

app_name = 'api'

urlpatterns = [
    path(route='create_user/', name='create_user',
         view=views.CreateCustomUserView.as_view(),),
    path(route='create_token/', name='create_token',
         view=views.CreateTokenView.as_view(),),
    path(route='me/', name='me',
         view=views.ManageUserView.as_view(),),
    path('', include(router.urls)),
]
