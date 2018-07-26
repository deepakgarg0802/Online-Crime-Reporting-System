
from django.conf.urls import url, include
from django.contrib import admin
from comment.views import CreateComment
from comment.views import HomePage, CommentPage
from home.views import criminal_directory
from home.views import upload_evidence
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from police.views import person_detail_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^about$', TemplateView.as_view(template_name="about.html")),
    url(r'^contact', TemplateView.as_view(template_name="contact.html")),
    url(r'^police/', include('police.urls')),
    url(r'^anonymous/', include('home.url_anonymous')),
    url(r'^citizen/', include('citizen.urls')),
    url(r'comment/ajax/create', CreateComment, name = "create_comment"),
    url(r'comment/', CommentPage, name = "comment"),
    url(r'^criminal_directory/', criminal_directory, name = "criminal_directory"),
    url(r'evidence/(?P<id>\d+)/upload', upload_evidence, name = "upload_anonymous_evidence"),
    url(r'^person_detail/(?P<id>\w+)/$', person_detail_view, name='person_detail'),

    url(r'^$', HomePage, name = "HomePage")

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)