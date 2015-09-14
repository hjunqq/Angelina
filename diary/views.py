from django.shortcuts import render,render_to_response,HttpResponseRedirect,HttpResponse
from django.template import RequestContext,Template
from django.contrib.auth import authenticate,login,logout
from django.http import Http404
from django.db.models import Q
from django.utils import timezone

import datetime
import calendar
import pytz

from .models import *
from django import forms
from user_agents import parse
from itertools import izip

# define user login form
class UserForm(forms.Form):
    username = forms.CharField(label='username',max_length=100)
    password = forms.CharField(label='password',widget=forms.PasswordInput())
# define log form
class DayMoodForm(forms.Form):
    score = forms.IntegerField(label='score')
    keywords = forms.CharField(label='abstract',max_length=300)
    contenttext = forms.CharField(label='contenttext',max_length=100000)

# create or delete functions
def addKeyword(user,addtime,text):
    try:
        keyword = KeyWord.objects.get(text = text)
    except:
        keyword = KeyWord.objects.create( author = user,addtime = addtime, text = text)
    return keyword
    

def getAllKeyword():
    keywords = KeyWord.objects.all()
    return keywords

def addDayMood(user,addtime,score,keywords,content):
    daymood = DayMood.objects.create(date=addtime.date(),
                                     time=addtime.time(),
                                     author=user,
                                     score=score,
                                     content=content)
    for keyword in keywords:
        daymood.keywords.add(keyword)
    daymood.save()
    dayscore = addDayScore(user,addtime.date(),score,daymood)
    return daymood

def keywordtoText(daymood):
    keywords = daymood.keywords.all()
    itext = []
    for item in keywords:
        itext.append(item.text)
    keywordtext = ','.join(itext)
    return keywordtext

def getMyDayMood(user,date):
    daymoods = DayMood.objects.filter(date=date).filter(author=user)
    return daymoods

def getOtherDayMood(user,date):
    daymoods = DayMood.objects.filter(date=date).exclude(author=user)
    return daymoods

def addDayScore(user,date,score,mood):
    dayscore = DayScore.objects.get_or_create(date = date,
                                              author = user)
    if dayscore[1]:
        dayscore[0].count = 1
        dayscore[0].score = float(score)
        dayscore[0].moods.add(mood)
        dayscore[0].save()
    else:
        sumscore = dayscore[0].score * float(dayscore[0].count) + float(score)
        dayscore[0].count += 1
        dayscore[0].score = sumscore / float(dayscore[0].count)
        dayscore[0].moods.add(mood)
        dayscore[0].save()
    monthscore = updateMonthScore(user,date,dayscore[0].score)
    return dayscore[0]

def getMyDayScore(user,date):
    try:
        dayscore = DayScore.objects.get(date=date,author=user).score
    except DayScore.DoesNotExist:
        dayscore = 0
    return dayscore

def getOtherDayScore(user,date):
    try:
        dayscore = DayScore.objects.get(Q(date=date) & ~Q(author=user)).score
    except DayScore.DoesNotExist:
        dayscore = 0 
    return dayscore

def updateMonthScore(user,date,score):
    monthscore = MonthScore.objects.get_or_create(author = user,
                                                  year = date.year,
                                                  month = date.month)
    if monthscore[1]:
        monthscore[0].count = date.day
        monthscore[0].tscore = score
        monthscore[0].score = score
        monthscore[0].save()
    else:
        if monthscore[0].count == date.day:
            monthscore[0].score = monthscore[0].score- monthscore[0].tscore
            monthscore[0].score += score
            monthscore[0].tscore = score
        else:
            monthscore[0].count = date.day
            monthscore[0].score += score
            monthscore[0].tscore = score
        monthscore[0].save()
    yearscore = updateYearScore(user,date,monthscore[0].score)
    return monthscore[0]

def getMyMonthScore(user,date):
    year = date.year
    month = date.month
    try:
        monthscore = MonthScore.objects.get(author = user,
                                            year = year,
                                            month = month).score
    except MonthScore.DoesNotExist:
        monthscore = 0
    return monthscore

def getOtherMonthScore(user,date):
    year = date.year
    month = date.month
    try:
        monthscore = MonthScore.objects.get(~Q(author = user) & Q(year = year) & Q(month = month)).score
    except MonthScore.DoesNotExist:
        monthscore = 0
    return monthscore

def updateYearScore(user,date,score):
    yearscore = YearScore.objects.get_or_create(author =user,year = date.year)
    if yearscore[1]:
        yearscore[0].count = date.month
        yearscore[0].tscore = score
        yearscore[0].score = score
        yearscore[0].save()
    else:
        if yearscore[0].count == date.month:
            yearscore[0].score = yearscore[0].score - yearscore[0].tscore
            yearscore[0].score += score
            yearscore[0].tscore = score
        else:
            yearscore[0].score += score
            yearscore[0].count = date.month
            yearscore[0].tscore = score
        yearscore[0].save()
    return yearscore[0]

def getMyYearScore(user,date):
    year = date.year
    try:
        yearscore = YearScore.objects.get(author = user,year = year).score
    except YearScore.DoesNotExist:
        yearscore = 0
    return yearscore

def getOtherYearScore(user,date):
    year = date.year
    try:
        yearscore = YearScore.objects.get(~Q(author = user) & Q(year = year)).score
    except YearScore.DoesNotExist:
        yearscore = 0
    return yearscore


def index(request):
    if request.user.is_authenticated():
        user = request.user    
    else:
        return HttpResponseRedirect('/diary/login/')     
    addtime =  timezone.localtime(timezone.now())
    date = addtime.date()
    lastday = date + datetime.timedelta(-1)
    nextday = date + datetime.timedelta(+1)    
    mf = DayMoodForm()
    myDayMood = getMyDayMood(user,date)
    yourDayMood = getOtherDayMood(user,date)
    myMonthScore = getMyMonthScore(user,date)
    yourMonthScore = getOtherMonthScore(user,date)   
    keywords = getAllKeyword()
    if request.method =='POST':
        mf = DayMoodForm(request.POST)
        if mf.is_valid():
            score = mf.cleaned_data['score']
            keywordtexts = mf.cleaned_data['keywords'].split(',')
            content = mf.cleaned_data['contenttext']      

            keywords =[]
            for keyword in keywordtexts:
                ikey = addKeyword(user,addtime,keyword)
                keywords.append(ikey)

            daymood = addDayMood(user,addtime,score,keywords,content)
            
            response = HttpResponseRedirect('/diary/')
            return response    
        else:
            mf = DayMoodForm()
    return render_to_response('diary.html',locals(),context_instance=RequestContext(request))

def dayarchive(request,year,month,day):
    if request.user.is_authenticated():
        user = request.user    
    else:
        return HttpResponseRedirect('/diary/login/')
    year = int(year)
    month = int(month)
    day = int(day)
    date = datetime.datetime(year,month,day)     
    lastday = date + datetime.timedelta(-1)
    nextday = date + datetime.timedelta(+1)   
    myDayMood = getMyDayMood(user,date)
    yourDayMood = getOtherDayMood(user,date)  
    myMonthScore = getMyMonthScore(user,date)
    yourMonthScore = getOtherMonthScore(user,date)        
    date = timezone.localtime(timezone.now()).date()
    return render_to_response('day_archive.html',locals(),context_instance=RequestContext(request))    


def montharchive(request,year,month):
    if request.user.is_authenticated():
        user = request.user    
    else:
        return HttpResponseRedirect('/diary/login/')
    year=int(year)
    month=int(month)
    date = timezone.localtime(timezone.now())
    myYearScore = getMyYearScore(user,date)
    yourYearScore = getOtherYearScore(user,date) 
    
    days=calendar.monthcalendar(year, month)
    myWeekScore = []
    yourWeekScore = []
    bothScore = []
    calDay = []    

    for weeks in days:
        myDayScore =[]
        yourDayScore = []
        for day in weeks:
            calDay.append(day)    
            if day !=0:
                date = datetime.date(year,month,day)
                iDayScore = getMyDayScore(user,date)
                myDayScore.append(iDayScore)
                iDayScore = getOtherDayScore(user,date)
                yourDayScore.append(iDayScore)
            else:
                myDayScore.append(0.0)
                yourDayScore.append(0.0)
        myWeekScore.append(myDayScore)
        yourWeekScore.append(yourDayScore)
        bothScore.append(zip(myDayScore,yourDayScore,weeks))
    weeks = len(days)    
    bothScoreChart = bothScore
    lastMonth = month -1
    if lastMonth == 0:
        lastMonth = 12
        year = year-1
    lastMonth = datetime.datetime(year,lastMonth,1)
    nextMonth = month + 1
    if nextMonth == 13:
        nextMonth = 1
        year = year + 1

    nextMonth = datetime.datetime(year,nextMonth,1)
    date = timezone.localtime(timezone.now())
    return render_to_response('month_archive.html',locals(),context_instance=RequestContext(request))        

def yeararchive(request,year):
    if request.user.is_authenticated():
        user = request.user    
    else:
        return HttpResponseRedirect('/diary/login/')    
    year=int(year)
    month = [i+1 for i in range(0,12)]
    myMonthScore =[]
    yourMonthScore =[]
    MonthTotalScore=[]
    for m in month:
        date = datetime.date(year,m,1)
        myMonthScore.append(getMyMonthScore(user, date))
        yourMonthScore.append(getOtherMonthScore(user, date))
        days = calendar.monthrange(year, m)[1]
        MonthTotalScore.append(days*5)
    myYearScore=getMyYearScore(user, date)
    yourYearScore=getOtherYearScore(user, date)
    bothMonthScore=zip(myMonthScore,yourMonthScore,month,MonthTotalScore)
    lastyear = year-1
    nextyear = year+1
    date = timezone.localtime(timezone.now())
    return render_to_response('year_archive.html',locals(),context_instance=RequestContext(request))      
    

def login_page(request):
    if request.user.is_authenticated():
        response = HttpResponseRedirect('/diary/')
        return response
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            user = authenticate(username=username,password=password)
            login(request, user)
            if request.META.has_key('HTTP_CF_CONNECTING_IP'):
                logInIP = request.META['HTTP_CF_CONNECTING_IP']
            else:
                logInIP = request.META['REMOTE_ADDR']
            logInTime = datetime.datetime.now()
            logOutTime = datetime.datetime.now()
            UserAgent = str(parse(request.META.get('HTTP_USER_AGENT')))
            try:
                UItem= UserLogInfo.objects.create(user = user,
                                                  logInIP = logInIP,
                                                  logInTime = logInTime,
                                                  logOutTime = logOutTime, 
                                                  UserAgent = UserAgent)
            except:
                pass
            response = HttpResponseRedirect('/diary/')
            LogID = UItem.pk
            response.set_cookie('LogID',LogID,3600)
            return response
        else:
            uf = UserForm()
    else:
        uf = UserForm()
    return render_to_response('login_page.html',locals(),context_instance=RequestContext(request))
def logout_page(request):
    LogID = request.COOKIES.get('LogID')
    try :
        UItem = UserLogInfo.objects.get(pk=LogID)
        UItem.logOutData = datetime.datetime.now()
        UItem.save()
    except:
        pass
    logout(request)
    return HttpResponseRedirect('/diary/login/')