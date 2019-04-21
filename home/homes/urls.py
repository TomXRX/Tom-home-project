from django.urls import path

from . import views
app_name = "homes"
urlpatterns = [
    path('', views.index, name='index'),
    path('control/',views.ControlView.as_view(),name="control"),
    path('set/', views.set, name='set'),
    path('get/', views.get, name='get'),
    path('<int:pk>/change/',views.change,name='change'),
]