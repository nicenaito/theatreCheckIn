from django import forms
import datetime
import theatreplaces
import movilelist
from .models import CheckIns

class MovieForm(forms.ModelForm):
    
    now = datetime.datetime.now()
    current_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
    checkin_datetime = forms.DateTimeField(label='鑑賞日時', widget=forms.DateInput, initial=current_datetime, input_formats='%Y-%m-%d %H:%M:%S')

    latitude, longitude = theatreplaces.current_place()
    theatre_list = tuple(theatreplaces.get_movie_theatre(latitude, longitude))
    theatre = forms.CharField(label='劇場')
    movie_id = forms.ChoiceField(label='作品名', choices=CheckIns.movie_list)

    class Meta:
        model = CheckIns
        fields = "__all__"
        exclude = ('author', 'pub_date', 'movie')

class TheatreSearchForm(forms.Form):
    theatre = forms.ChoiceField(label='劇場')
