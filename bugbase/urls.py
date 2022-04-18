from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import SampleListView, SampleDetailView

from bugbase import views

urlpatterns = [
    path('list/', SampleListView.as_view(), name = 'sample-list'),
    path('list/<int:pk>', SampleDetailView.as_view(template_name = 'bugbase/sample-detail.html'), name = 'sample-detail'),
    path('junk/', views.junk, name='junk'),
    path('stupid/', views.stupid, name='stupid'),
    path('landing/', views.send_dictionary, name='landing')
]