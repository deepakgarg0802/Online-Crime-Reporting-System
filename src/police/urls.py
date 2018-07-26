from django.conf.urls import url, include
from django.views.generic import TemplateView
from .views import *
urlpatterns = [

    url(r'^$', login_view , name='login'),
    url(r'^dashboard/$', dashboard , name='police_dashboard'),
	url(r'^logout/$', police_logout , name='police_logout'),

	url(r'^cbc/(?P<id>\d+)/$', cbcview , name='cbc'),
	url(r'^cybercbc/(?P<id>\d+)/$', cybercbcview , name='cybercbc'),


	url(r'^ajax/get_category/', get_case_categories, name = "get_categories"),

	url(r'^case_detail/(?P<id>\d+)/(?P<approved>\d+)/$', case_detail , name='case_detail'),

	url(r'^create_criminal_details/$', create_criminal_details , name='create_criminal_details'),

	url(r'^atips/$', atips , name='atips'),
	url(r'^atip_detail/(?P<id>\d+)/$', atip_detail, name='atip_detail'),


]
