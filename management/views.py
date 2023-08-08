from django.shortcuts import render, get_object_or_404
from django.views import View
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login, authenticate
from .forms import UserChangeForm, UserLoginForm, UserCreationForm, GenerEditForm, AddAlbumForm
from home.models import Song, Genre, Singer, Album
from home.forms import SongEditForm
from .models import User


class ManagementHomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'management/home.html')


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('home:home')


class LoginView(View):
    def get(self, request):
        return render(request, 'management/login.html')

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form:
            user = authenticate(request, phone_number=form.data['phone_number'], password=form.data['password'])
            if user is not None:
                login(request, user)
                return redirect('management:management-home')
            else:
                return HttpResponse('user not found')
        return HttpResponse('s')


class UserCreationView(View):
    def get(self, request):
        return render(request, 'management/UserCreation.html')

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return True
        else:
            return render(request, 'management/UserCreation.html', {'form':form})

        return HttpResponse('something is wrong')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserChangeForm(instance=request.user)
        return render(request, 'management/profile.html', {'form': form})

    def post(self, request):
        form = UserChangeForm(request.POST)
        user = request.user
        if form.is_valid():
            cd = form.cleaned_data
            user.update(cd['first_name'], cd['last_name'], cd['phone_number'], cd['email'])
            form = UserChangeForm(request.POST)
            return render(request, 'management/profile.html', {'form': form})
        else:
            user.update(form.data['first_name'], form.data['last_name'], form.data['phone_number'], form.data['email'])

        return redirect('management:profile')


class NewSongView(View):
    form_class = SongEditForm

    def get(self, request):
        return render(request, 'management/song-new.html', {'form':self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            song = form.save(commit=False)
            song.writer = request.user
            song.save()
            return redirect('management:all-songs')
        return render(request, 'management/song-new.html', {'form': form})


class EditSogView(LoginRequiredMixin, View):
    form_class = SongEditForm

    def get(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        form = self.form_class(instance=song)
        return render(request, 'management/song-edit.html', {'song': song, 'form': form})

    def post(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        form = self.form_class(request.POST, instance=song)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'management/song-edit.html', {'song': song, 'form': form})
            raise ValueError('something is wrong')
        return redirect('management:edit_song', song_id)


class AllSongListView(LoginRequiredMixin, View):
    def get(self, request):
        songs = Song.objects.all()
        return render(request, 'management/all-songs-list.html', {'songs': songs})


class SongPreviewView(LoginRequiredMixin, View):
    def get(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        if song.situation == 'Published':
            return redirect('home:single-detail', song.slug)
        return render(request, 'home/single.html', {'song': song})


class SongDeleteView(LoginRequiredMixin, View):
    def get(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        song.delete()
        return redirect('management:all-songs')


class AddFavoriteView(View):
    def get(self, request, model, intended_id):
        if model == 'song':
            song = get_object_or_404(Song, id=intended_id)
            if song.favorites.filter(id=request.user.id).exists():
                song.favorites.remove(request.user)
            else:
                song.favorites.add(request.user)

        elif model == 'singer':
            singer = get_object_or_404(Singer, id=intended_id)
            if singer.favorites.filter(id=request.user.id).exists():
                singer.favorites.remove(request.user)
            else:
                singer.favorites.add(request.user)

        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class FavoritesListView(LoginRequiredMixin, View):
    def get(self, request):
        songs = Song.get_list().filter(favorites=request.user)
        singers = Singer.objects.filter(favorites=request.user)
        return render(request, 'management/favoriteslist.html', {'songs': songs, 'singers': singers})


class AllGenerListView(LoginRequiredMixin, View):
    def get(self, request):
        geners = Genre.objects.all()
        return render(request, 'management/all-gener-list.html', {'geners': geners})


class NewGenerView(View):
    form_class = GenerEditForm

    def get(self, request):
        return render(request, 'management/gener-new.html', {'form':self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('management:all-gener')
        return render(request, 'management/gener-new.html')


class EditGenerView(LoginRequiredMixin, View):
    form_class = GenerEditForm

    def get(self, request, gener_id):
        gener = get_object_or_404(Genre, id=gener_id)
        form = self.form_class(instance=gener)
        return render(request, 'management/gener-edit.html', {'gener': gener, 'form': form})

    def post(self, request, gener_id):
        gener = get_object_or_404(Genre, id=gener_id)
        form = self.form_class(request.POST, instance=gener)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'management/gener-edit.html', {'gener': gener, 'form': form})


class GenerDeleteView(LoginRequiredMixin, View):
    def get(self, request, gener_id):
        gener = get_object_or_404(Genre, slug=gener_id)
        gener.delete()
        return redirect('management:all-gener')


class PlaylistView(View):
    def get(self, request):
        if 'playlist' not in request.session:
            request.session['playlist'] = []
        return HttpResponse(request.session['playlist'])


class AddPlaylistView(View):
    def get(self, request, song_id):
        if 'playlist' not in request.session:
            request.session['playlist'] = []

        if Song.objects.filter(id=song_id).exists():
            if song_id not in request.session['playlist']:
                request.session['playlist'] += [song_id]

        return redirect('management:playlist')


class ClearPlaylistView(View):
    def get(self, request):
        if 'playlist' in request.session:
            request.session = []
            return redirect('management:playlist')


class AllAlumView(View):
    def get(self, request):
        albums = Album.objects.all()
        return render(request, 'management/all-album-list.html', {'albums': albums})


class AddNewAlbumView(View):
    form_class = AddAlbumForm

    def get(self, request):
        return render(request, 'management/add-album.html', {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('management:all-albums')
        return render(request, 'management/add-album.html', {'form': form})


class EditAlbumView(View):
    form_class = AddAlbumForm

    def get(self, request, album_id):
        album = get_object_or_404(Album, id=album_id)
        form = self.form_class(instance=album)
        return render(request, 'management/edit-album.html', {'form': form, 'album': album})

    def post(self, request, album_id):
        album = get_object_or_404(Album, id=album_id)
        form = self.form_class(request.POST, instance=album)
        if form.is_valid():
            form.save()
            return redirect('management:all-albums')
        return render(request, 'management/edit-album.html', {'form': form, 'album': album})
