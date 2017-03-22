"""
Contains the URL patterns for the Campaign Commander.
"""

from django.conf.urls import url, include
from commander import views
from django.contrib import auth


urlpatterns = [
    url(r'accounts/profile', views.user_profile, name='user_profile'),
    url(r'home', views.home, name='home'),
    url(r'^image-requests', views.image_requests,
        name='image_requests'),
    url(r'add-image-request', views.add_image_request,
        name='add_image_request'),
    url(r'user-image-request', views.user_image_request,
        name='user_image_request'),
    url(r'api/image-requests/(?P<pk>[0-9]+)/$',
        views.ImageRequestDetail.as_view(),
        name='api_image_requests_detail'),
    url(r'api/image-requests/(?P<username>.+)/$',
        views.ImageRequestListByAuthor.as_view(),
        name='api_image_requests_by_author'),
    url(r'api/image-requests',
        views.ImageRequestList.as_view(),
        name='api_image_requests'),
    url(r'api/submitted-images',
        views.SubmittedImageList.as_view(),
        name='api_submitted_images'),
    url(r'^login/$', views.login_oauth, name='login'),
    url(r'^logout/$', auth.logout, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^register/(?P<backend>[^/]+)/$', views.register),
    url(r'logout-oauth/', views.logout_oauth),
    url(r'', views.index, name='index'),
]
