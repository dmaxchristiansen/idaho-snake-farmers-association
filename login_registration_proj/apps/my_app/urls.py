from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^loggedin$', views.loggedin),
    url(r'^logout$', views.logout),
    url(r'^welcome$', views.welcome),
    url(r'^wall$', views.wall),
    url(r'^post_message$', views.postMessage),
    url(r'^post_comment/(?P<number>\d+)$', views.postComment),
]