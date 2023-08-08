from django.urls import path
from . import views


app_name = 'management'
urlpatterns = [
    path('', views.ManagementHomeView.as_view(), name='management-home'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.UserCreationView.as_view(), name='user-creation'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),

    path('songs/', views.AllSongListView.as_view(), name='all-songs'),
    path('songs/add-new/', views.NewSongView.as_view(), name='new-song'),
    path('song/edit/<int:song_id>/', views.EditSogView.as_view(), name='edit_song'),
    path('song/preview/<int:song_id>/', views.SongPreviewView.as_view(), name='song_preview'),
    path('song/delete/<int:song_id>/', views.SongDeleteView.as_view(), name='song-delete'),

    path('favorites/', views.FavoritesListView.as_view(), name='favorites-list'),
    path('add-favorite/<str:model>/<int:intended_id>/', views.AddFavoriteView.as_view(), name='add-favorite'),

    path('playlist/', views.PlaylistView.as_view(), name='playlist'),
    path('add-playlist/<int:song_id>/', views.AddPlaylistView.as_view(), name='add-playlist'),
    path('clear-playlist/', views.ClearPlaylistView.as_view(), name='clear-playlist'),

    path('geners/', views.AllGenerListView.as_view(), name='all-gener'),
    path('gener/add-new/', views.NewGenerView.as_view(), name='new-gener'),
    path('gener/edit/<int:gener_id>/', views.EditGenerView.as_view(), name='edit_gener'),
    path('gener/delete/<slug:song_id>/', views.GenerDeleteView.as_view(), name='gener-delete'),

    path('albums/', views.AllAlumView.as_view(), name='all-albums'),
    path('album/add-new/', views.AddNewAlbumView.as_view(), name='add-album'),
    path('album/edit/<int:album_id>/', views.EditAlbumView.as_view(), name='edit-album'),


]
