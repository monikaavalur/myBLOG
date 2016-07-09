from django.conf.urls import url
import views

urlpatterns=[
    url(r'^$', views.posts_list,name='list'),
    url(r'^create/$',views.posts_create,name='create'),
    url(r'^(?P<slug>[\w-]+)/$', views.posts_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', views.posts_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', views.posts_delete,name='delete'),
]