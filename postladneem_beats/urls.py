from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from postladneem_beats import views

urlpatterns = [
    path("", views.login_page),
    path("feed/", views.feed_page),
    path("creation/", views.creation_page),
    path("edit/", views.edit_page),
    path("edit_action/", views.edit_action),
    path("delete/", views.remove_action),
    path("beats/", views.create_beat),
    path("login/", views.login_page),
    path("login_action/", views.login_action),
    path("logout/", views.logout_action),
    path("registration/", views.registration_page),
    path("registration_action/", views.registration_action),
    path("mine/", views.mine),
    path("download/", views.download),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
