from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login',views.login, name='login'),
    path('login_action',views.login_action, name='login_action'),
    path('logout',views.logout, name='logout'),
    path('search', views.search, name='search'),
    path('search_camera', views.search_camera, name='search_camera'),
    path('vehicle_details/<id>', views.vehicle_details, name='vehicle_details'),
    path('camera_details', views.camera_details, name='camera_details'),
    path('camera_stream', views.livefe, name='camera_stream'),
    path('choose_camera', views.choose_camera, name='choose_camera'),
    path('stream', views.stream, name='stream'),
    path('stream_end', views.stream_end, name='stream_end'),
    path('add_cam', views.add_cam, name='add_cam'),
    path('add_cam_action', views.add_cam_action, name='add_cam_action'),
    path('new_details', views.new_details , name='new_details'),
    path('new_details_action', views.new_details_action , name='new_details_action'),
    path('path', views.path, name='path'),
    path('path_generator', views.path_generator, name='path_generator'),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)