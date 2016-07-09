from django.conf.urls import url
import views

urlpatterns=[
    url(r'^$', views.bloglistAPIVIEW.as_view(),name='list'),
    url(r'^create/$',views.blogcreateAPIVIEW.as_view(),name='create'),
    url(r'^(?P<slug>[\w-]+)/$',views.blogdetailAPIVIEW.as_view(),name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$',views.blogupdateAPIVIEW.as_view(),name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$',views.blogdeleteAPIVIEW.as_view(),name='delete')

]