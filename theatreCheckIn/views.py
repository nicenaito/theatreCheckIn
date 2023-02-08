from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.shortcuts import render  
from django.views import View
from django.views import generic
from .models import CheckIns
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
        context = {'form': form,}
        return render(request, 'theatreCheckIn/register.html', context)
register = CheckInInputView.as_view()

class CheckInConfirmView(generic.FormView):
    template_name = 'theatreCheckIn/register_confirm.html'
    context_object_name = 'register_confirm'
    
    form_class  = MovieForm
    
    def form_valid(self, form):
        form_class  = MovieForm
        context = {'form': form,}
        return render(self.request, 'theatreCheckIn/register_confirm.html', context)

    def form_invalid(self, form):
        form_class  = MovieForm
        context = {'form': form,}
        return render(self.request, 'theatreCheckIn/register.html', context)

class CheckInCompleteView(generic.CreateView):
    form_class = MovieForm
    success_url = reverse_lazy('theatreCheckIn:register')
    
    def form_valid(self, form):
       qryset =  form.save(commit=False)
       qryset.author_id = self.request.user.id
       qryset.pub_date = CheckIns.pub_date_list[self.request.POST.get('movie_title', None)]
       qryset.save()
       context = {'form': form,}
       return render(self.request, 'theatreCheckIn/index.html', context)

    def form_invalid(self, form):
        return render(self.request, 'theatreCheckIn/register.html', {'form': form})
    
class CheckInListView(generic.ListView):
    template_name = 'theatreCheckIn/checkin_list.html'
    model = CheckIns
    ordering = '-movie_title'
    
class CheckInDetailView(generic.DetailView):
    model = CheckIns
    template_name = 'theatreCheckIn/checkin_detail.html'
    def get_object(self):
        return CheckIns.objects.get(pk=self.kwargs["pk"])

