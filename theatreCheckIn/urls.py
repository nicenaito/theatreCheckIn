from django.urls import path
from . import views


app_name = 'theatreCheckIn'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register/', views.CheckInInputView.as_view(), name='register'),
    path('register_complete/', views.CheckInCompleteView.as_view(), name='register_complete'),
    path('checkin_list/', views.CheckInListView.as_view(), name='checkin_list'),
    path('checkin_detail/<str:pk>', views.CheckInDetailView.as_view(), name='checkin_detail'),
    path('checkin_delete/<str:pk>', views.CheckInDeleteView.as_view(), name='checkin_delete'),


]