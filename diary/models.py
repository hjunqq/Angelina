from django.db import models
# Use Django User
from django.contrib.auth.models import User
# Create your models here.

class UserLogInfo(models.Model):
    user = models.ForeignKey(User)
    logInIP = models.CharField(max_length=150)
    logInTime = models.DateTimeField()
    logOutTime = models.DateTimeField()
    UserAgent = models.CharField(max_length=150)
    
    def __unicode__(self):
        return str(self.pk)
    
    class Meta:
        db_table = 'UserLogInfo'
        verbose_name_plural='UserLogInfoes'

class KeyWord(models.Model):
    addtime = models.DateTimeField(blank="true")
    author = models.ForeignKey(User,blank="true")
    text = models.CharField(max_length=150,unique=True)
    
    def __unicode__(self):
        return self.text

class DayMood(models.Model):
    date = models.DateField()
    time = models.TimeField()
    author = models.ForeignKey(User)
    score = models.IntegerField()
    keywords = models.ManyToManyField(KeyWord)
    content = models.CharField(max_length=100000,blank="true")    

    
    def __unicode__(self):
        return str(self.date)
    def get_keywords_text(self):
        text = []
        for keyword in self.keywords.all():
            text.append(keyword.text)
        return ','.join(text)

    
class DayScore(models.Model):
    date = models.DateField()
    author = models.ForeignKey(User)
    score = models.FloatField(default=0)
    count = models.IntegerField(default=0)
    moods = models.ManyToManyField(DayMood)
    
    def __unicode__(self):
        return str(self.date)
    
class MonthScore(models.Model):
    month = models.IntegerField()
    year = models.IntegerField()
    author = models.ForeignKey(User)
    score = models.FloatField(null="true")
    tscore=models.FloatField(null="true")
    count = models.IntegerField(null="true")
    
    def __unicode__(self):
        return str(self.year)+str(self.month)

class YearScore(models.Model):
    year = models.IntegerField()
    author = models.ForeignKey(User)
    score = models.FloatField(null="true")
    tscore=models.FloatField(null="true")
    count = models.IntegerField(null="true")
    
    def __unicode__(self):
        return str(self.year)