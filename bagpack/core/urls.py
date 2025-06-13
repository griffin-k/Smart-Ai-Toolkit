from django.urls import path
from . import views 


from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.gallery_view, name='gallery'),
    path('tts/', views.tts_view, name='tts'),
    path('story/', views.story_view, name='story'),
    path('image/', views.image_view, name='image'),
    path('story/download/', views.download_story_pdf, name='download_story'),
    path('album/<str:album_name>/',views.album_detail, name='album_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
