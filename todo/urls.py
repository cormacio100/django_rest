from django.conf.urls import url
from todo.views import TodoView

urlpatterns = [
    #   When utilising a CBV - Class Based View we need
    #   to invoke the as_view() method on the View
    #   Any view that inherits from the base View object
    #   will have the as_view method. This will allow
    #   Django to use the class-based view as a standard
    #   function-based view.
    url(r'^$',TodoView.as_view()),
    url(r'(?P<pk>[0-9]+)/$',TodoView.as_view())
]