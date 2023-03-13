from theatreCheckIn.models import CheckIns, Movies
from rest_framework import serializers
from django.utils import timezone

class CheckinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckIns
        fields = "__all__"

class MoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        # fields = "__all__"
        exclude = ('created_datetime', 'updated_datetime')
    
    def create(self, validated_data):
        newMovie = Movies.objects.create(
            movie_id = 1,
            movie_title = validated_data["movie_title"],
            pub_date = validated_data["pub_date"],
            original_title = validated_data["original_title"],
            poster_path = validated_data["poster_path"],
            original_language = validated_data["original_language"],
            overview = validated_data["overview"],
            checkin_count = validated_data["checkin_count"],
            now_playing = validated_data["now_playing"],
            created_datetime = timezone.now(),
            updated_datetime = timezone.now()
        )
        
        newMovie.save()
        return newMovie