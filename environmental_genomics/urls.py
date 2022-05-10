from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.conf.urls import url
from markdownx import urls as markdownx

# from users import views as user_views
# from django.contrib.auth import views as auth_views

from . import views
from bugbase.models import Sample_Data

admin.autodiscover()

urlpatterns = [
    path("sitemap.xml", sitemap, {"sitemaps": {"cmspages": CMSSitemap}}),
]

urlpatterns += [
    path('markdownx/', include(markdownx)),
]

urlpatterns += [
    path('bugbase/', include('bugbase.urls'))
]

urlpatterns += [
    path("admin/", admin.site.urls),
    #path("", include("cms.urls")),

    path('accounts/', include('django.contrib.auth.urls')),
    path('samples/', views.index),
    path('sample/<int:sample_id>', views.sample_data)
]



# urlpatterns += [
#     path('profile/', user_views.profile, name='profile'),
#     path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
#     path('password-reset/',
#          auth_views.PasswordResetView.as_view(
#              template_name='users/password_reset.html'
#          ),
#          name='password_reset'),
#     path('password-reset/done/',
#          auth_views.PasswordResetDoneView.as_view(
#              template_name='users/password_reset_done.html'
#          ),
#          name='password_reset_done'),
#     path('password-reset-confirm/<uidb64>/<token>/',
#          auth_views.PasswordResetConfirmView.as_view(
#              template_name='users/password_reset_confirm.html'
#          ),
#          name='password_reset_confirm'),
#     path('password-reset-complete/',
#          auth_views.PasswordResetCompleteView.as_view(
#              template_name='users/password_reset_complete.html'
#          ),
#          name='password_reset_complete'),
# ]

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
