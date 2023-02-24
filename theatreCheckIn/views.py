from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import View
from django.views import generic
from .models import CheckIns
from .models import Movies
from .forms import MovieForm, TheatreSearchForm
import theatreplaces
import datetime


class IndexView(generic.ListView):
    template_name = 'theatreCheckIn/index.html'
    context_object_name = 'latest_movie_list'

    def get_queryset(self):
        """Return the movies."""
        return CheckIns.objects.all()

class TheatreSearchView(generic.FormView):
    template_name = 'theatreCheckIn/search_theatre.html'
    def get(self, request, *args, **kwargs):
        form = TheatreSearchForm()
        context = {'form': form,}
        return render(request, 'theatreCheckIn/search_theatre.html', context)
register = TheatreSearchView.as_view()

class CheckInInputView(View):
    template_name = 'theatreCheckIn/register.html'
    context_object_name = 'register'

    def get(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        current_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
        form = MovieForm(request.POST or {"theatre": request.GET.get("theatre"), "checkin_datetime":current_datetime})
        # form.theatre = request.GET.get("theatre")
        context = {'form': form,}
        return render(request, 'theatreCheckIn/register.html', context)
register = CheckInInputView.as_view()

class CheckInCompleteView(generic.CreateView):
    form_class = MovieForm
    success_url = reverse_lazy('theatreCheckIn:index')

    def form_valid(self, form):
        selected_movie_id = int(self.request.POST.get('movie_id', None))
        selected_movie_title = ""
        try:
            selected_movie = Movies.objects.get(pk=selected_movie_id)
            selected_movie_title = selected_movie.movie_title
        except (KeyError, Movies.DoesNotExist):
            new_movie = {}
            for item in CheckIns.movies:
                print(item["id"])
                if item["id"] == selected_movie_id:
                    new_movie = item
                    break
            print(new_movie)
            register_movie = Movies(
                movie_id=new_movie["id"],
                movie_title=new_movie["title"],
                pub_date=new_movie["release_date"],
                original_title=new_movie["original_title"],
                poster_path=new_movie["poster_path"],
                original_language=new_movie["original_language"],
                overview=new_movie["overview"],
                checkin_count=1
            )
            register_movie.save()
        else:
            selected_movie.checkin_count += 1
            selected_movie.save()

        qryset = form.save(commit=False)
        qryset.author_id = self.request.user.id
        qryset.movie_id = selected_movie_id
        qryset.save()
        template_name = 'theatreCheckIn/register_complete.html'
        context = {'form': form,
                   'selected_movie_title': selected_movie_title}

        return render(self.request, 'theatreCheckIn/register_complete.html', context)

    def form_invalid(self, form):
        return render(self.request, 'theatreCheckIn/register.html', {'form': form})


class CheckInListView(generic.ListView):
    template_name = 'theatreCheckIn/checkin_list.html'
    model = CheckIns
    ordering = '-checkin_datetime'

    def get_queryset(self):
        current_user = self.request.user
        return CheckIns.objects.filter(author=current_user.id)


class CheckInDetailView(generic.DetailView):
    model = CheckIns
    template_name = 'theatreCheckIn/checkin_detail.html'

    def get_object(self):
        return CheckIns.objects.get(pk=self.kwargs["pk"])


class CheckInDeleteView(generic.DeleteView):
    model = CheckIns
    template_name = 'theatreCheckIn/checkin_delete.html'
    success_url = reverse_lazy('theatreCheckIn:checkin_list')

    def get_object(self):
        return CheckIns.objects.get(pk=self.kwargs["pk"])
