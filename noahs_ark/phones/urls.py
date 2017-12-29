'''Urls for phone app'''
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from phones import views

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^category/$', views.PhoneCategoryView.as_view(), name='phone-category-list'),
    url(r'^category/(?P<pk>[0-9]+)/$',
        views.PhoneCategoryDetailView.as_view(),
        name='phonecategory-detail'),
    url(r'^category/(?P<pk>[0-9]+)/phones/$', views.PhoneListView.as_view(), name='phones'),
    url(r'^category/(?P<pk>[0-9]+)/phones/(?P<pk2>[0-9]+)/$',
        views.PhoneDetailView.as_view(),
        name='phones-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
