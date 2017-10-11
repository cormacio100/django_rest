from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from accounts.views import UserView

urlpatterns = [
    # e.g. URL accounts/register/
    url(r'^register/$',UserView.as_view()),
    # e.g. URL accounts/api-token-auth/ will invoke a view called obtain_jwt_token.
    # obtain_jwt_token view will create a JWT based on the username and password
    url(r'^api-token-auth/$',obtain_jwt_token)
]