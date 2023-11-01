"""Urls maping for the user API"""

from django.urls import path

from user.views import (
    CreateTokenView,
    CreateUserViwe,
    ManageUserView
)

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserViwe.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('me/', ManageUserView.as_view(), name='me')

]
