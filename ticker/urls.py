from django.conf.urls import url

from . import views

app_name = 'ticker'
urlpatterns = [
    url(r'^$', views.bokeh, name='homepage'),
    url(r'^graph/$', views.graph, name='graph'),
]