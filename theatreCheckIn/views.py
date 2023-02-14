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
from .forms import MovieForm


class IndexView(generic.ListView):
    template_name = 'theatreCheckIn/index.html'
    context_object_name = 'latest_movie_list'

    def get_queryset(self):
        """Return the movies."""
        return CheckIns.objects.all()


class CheckInInputView(View):
    template_name = 'theatreCheckIn/register.html'
    context_object_name = 'register'

    def get(self, request, *args, **kwargs):
        form = MovieForm()
        context = {'form': form, }
        return render(request, 'theatreCheckIn/register.html', context)


register = CheckInInputView.as_view()


class CheckInConfirmView(generic.FormView):
    template_name = 'theatreCheckIn/register_confirm.html'
    context_object_name = 'register_confirm'

    form_class = MovieForm

    def form_valid(self, form):
        form_class = MovieForm
        context = {'form': form, }
        return render(self.request, 'theatreCheckIn/register_confirm.html', context)

    def form_invalid(self, form):
        form_class = MovieForm
        context = {'form': form, }
        return render(self.request, 'theatreCheckIn/register.html', context)


class CheckInCompleteView(generic.CreateView):
    form_class = MovieForm
    success_url = reverse_lazy('theatreCheckIn:register')

    def form_valid(self, form):
        
        selected_movie_id = int(self.request.POST.get('movie_title', None))
        print(selected_movie_id)
        try:
            selected_movie = Movies.objects.get(pk=selected_movie_id)
        except (KeyError, Movies.DoesNotExist):
            # new_movie = [d.get("id") for d in CheckIns.movies]
            new_movie = {}
            for item in CheckIns.movies:
                print(item["id"])
                if item["id"] == selected_movie_id:
                    new_movie = item
                    break
            # new_movie = [ item for item in CheckIns.movies if item['id'] == selected_movie_id ]
            print(new_movie)
            register_movie= Movies(
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
        # qryset.pub_date = CheckIns.pub_date_list[self.request.POST.get('movie_title', None)]
        qryset.save()
        context = {'form': form,}
        
        return render(self.request, 'theatreCheckIn/index.html', context)

    def form_invalid(self, form):
        return render(self.request, 'theatreCheckIn/register.html', {'form': form})
    
class CheckInListView(generic.ListView):
    template_name = 'theatreCheckIn/checkin_list.html'
    model = CheckIns
    ordering = '-checkin_datetime'
# checkin_list = CheckInListView.as_view()
    
class CheckInDetailView(generic.DetailView):
    model = CheckIns
    template_name = 'theatreCheckIn/checkin_detail.html'
    def get_object(self):
        return CheckIns.objects.get(pk=self.kwargs["pk"])
    
class CheckInUpdateView(generic.UpdateView):
    model = CheckIns
    fields = ('checkin_datetime', 'theatre', 'movie_title', 'comment')
    template_name = 'theatreCheckIn/checkin_update.html'
    success_url = reverse_lazy('theatreCheckIn:checkin_update')
    def get_object(self):
        return CheckIns.objects.get(pk=self.kwargs["pk"])

# def update(request, checkin_id, generic.U):
#     checkin = get_object_or_404(CheckIns, pk=checkin_id)
#     try:
#         selected_checkin = checkin.choice_set.get(pk=request.POST['checkin'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'theatreCheckIn/checkin_list.html', {
#             'question': checkin,
#             'error_message': "チェックイン履歴が存在しません。",
#         })
#     else:
#         form_class = MovieForm
#         selected_checkin.author = form_class.fields
#         checkin.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))