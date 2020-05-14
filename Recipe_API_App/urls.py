"""Recipe API App - urls.py"""

from django.urls import path

from Recipe_API_App import views

app_name = 'api'

urlpatterns = [
    path(route='create_user/', name='create_user',
         view=views.CreateCustomUserView.as_view(),),
    path(route='create_token/', name='create_token',
         view=views.CreateTokenView.as_view(),),
    path(route='me/', name='me',
         view=views.ManageUserView.as_view(),),
]
