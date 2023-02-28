from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.utils import timezone

class Movies(models.Model):
    movie_id = models.IntegerField(primary_key=True, editable=False)
    movie_title = models.CharField(max_length=800, verbose_name='作品名')
    pub_date = models.DateField(verbose_name='公開日')
    original_title = models.CharField(max_length=800, verbose_name='オリジナル作品名')
    poster_path = models.TextField(null=True, verbose_name='ポスター画像パス')
    original_language = models.CharField(max_length=2, verbose_name='劇場')
    overview = models.TextField(null=True, verbose_name='あらすじ')
    checkin_count = models.IntegerField(default=0, verbose_name='チェックイン回数')
    now_playing = models.BooleanField(default=True, verbose_name='公開中フラグ')
    created_datetime = models.DateTimeField(default=timezone.now, verbose_name='登録日時')
    updated_datetime = models.DateTimeField(default=timezone.now, verbose_name='更新日時')

class CheckIns(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    checkin_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    checkin_datetime = models.DateTimeField(verbose_name='鑑賞日時')
    theatre = models.CharField(null=False, max_length=200, verbose_name='劇場')
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    comment = models.TextField(blank = True, null = True, verbose_name='感想')
    
    movies = []
