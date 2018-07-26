from django.conf.urls import url, include
from django.views.generic import TemplateView
from .views import *


urlpatterns = [

    url(r'^$', login_view , name='login'),
    url(r'^logout$', citizen_logout , name='login'),
    url(r'^register$', register_view , name='login'),
    url(r'^dashboard/$', dashboard , name='dashboard'),
    url(r'^create_case/$', create_case , name='create_case'),
    url(r'^cbcview/(?P<sel>\d+)/$', cbcview , name='cbcview'),
	url(r'^user_case_detail/(?P<id>\d+)/$', user_case_detail , name='user_case_detail'),
    url(r'^create_cyber_case/$', create_cyber_case , name='create_cyber_case'),

]
