from django.test import TestCase,RequestFactory
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser,User

import datetime
import calendar

from django.utils import timezone
from django.test import client

from .models import *
from .views import *

# Create your tests here.
class KeyWordTestCase(TestCase):
    def test_addfunc(self):
        user = User.objects.create_user('user')
        addtime=timezone.now()
        text='happy'        
        keyword = addKeyword(user,addtime,text)
        self.failUnlessEqual('happy',keyword.text)
        text='sad'      
        keyword = addKeyword(user,addtime,text)
        self.failUnlessEqual('sad',keyword.text)
        addtime=timezone.now()
        keyword = addKeyword(user,addtime,text)
        self.failUnlessEqual('sad',keyword.text)


# Test DayMood Funcitons
class DayMoodTestCase(TestCase):
    def test_add(self):
        user1 = User.objects.create_user('user1')
        user2 = User.objects.create_user('user2')
        text ='happy'
        addtime = timezone.now()
        keyword = addKeyword(user1,addtime,text)
        text ='sad'
        keyword = addKeyword(user2,addtime,text)
        keyword = getAllKeyword()
        score = 1.0
        content = "happy everyday"
        daymood = addDayMood(user1,addtime,score,keyword,content)
        keyword = daymood.keywords.all()
        self.failUnlessEqual('happy',keyword[0].text)
        self.failUnlessEqual('sad',keyword[1].text)
        keywordtext = keywordtoText(daymood)
        self.failUnlessEqual('happy,sad',keywordtext)
    def test_dayscore(self):
        user1 = User.objects.create_user('user1')
        user2 = User.objects.create_user('user2')
        text ='happy'
        addtime = timezone.now()
        keyword = addKeyword(user1,addtime,text)
        text ='sad'
        keyword = addKeyword(user2,addtime,text)
        keyword = getAllKeyword()
        score = 1.0
        content = "happy everyday"
        daymood = addDayMood(user1,addtime,score,keyword,content)
        keyword = daymood.keywords.all()
        self.failUnlessEqual('happy',keyword[0].text)
        self.failUnlessEqual('sad',keyword[1].text)

        dayscore = getMyDayScore(user1,addtime.date())
        self.failUnlessEqual(1,dayscore)
        score = 10.0
        daymood = addDayMood(user1,addtime,score,keyword,content)
        dayscore = getOtherDayScore(user1,addtime.date())
        self.failUnlessEqual(0,dayscore)

# Test MonthScore Funcitons
class MonthScoreTestCase(TestCase):
    def test_monthscore(self):
        user1 = User.objects.create_user('user1')
        user2 = User.objects.create_user('user2')
        text ='happy'
        addtime = timezone.now()
        keyword = addKeyword(user1,addtime,text)
        text ='sad'
        keyword = addKeyword(user2,addtime,text)
        keyword = getAllKeyword()
        score = 1.0
        content = "happy everyday"
        daymood = addDayMood(user1,addtime,score,keyword,content)
        monthscore = getMyMonthScore(user1,addtime.date())
        self.failUnlessEqual(1,monthscore)
        score = 10.0
        content = "happy everyday"
        daymood = addDayMood(user1,addtime,score,keyword,content)
        monthscore = getMyMonthScore(user1,addtime.date())
        self.failUnlessEqual(5.5,monthscore)
        addtime = addtime + datetime.timedelta(-1)
        score = 10.0
        daymood = addDayMood(user1,addtime,score,keyword,content)
        monthscore = getMyMonthScore(user1,addtime.date())
        self.failUnlessEqual(15.5,monthscore)
        monthscore = getOtherMonthScore(user1,addtime.date())
        self.failUnlessEqual(0,monthscore)
# Test YearScore Funcitons
class YearScoreTestCase(TestCase):
    def test_yearscore(self):
        user1 = User.objects.create_user('user1')
        user2 = User.objects.create_user('user2')
        text ='happy'
        addtime = timezone.now()
        keyword = addKeyword(user1,addtime,text)
        text ='sad'
        keyword = addKeyword(user2,addtime,text)
        keyword = getAllKeyword()
        score = 1.0
        content = "happy everyday"
        daymood = addDayMood(user1,addtime,score,keyword,content)
        yearscore = getMyYearScore(user1,addtime.date())
        self.failUnlessEqual(1,yearscore)
        score = 10.0
        content = "happy everyday"
        daymood = addDayMood(user1,addtime,score,keyword,content)
        yearscore = getMyYearScore(user1,addtime.date())
        self.failUnlessEqual(5.5,yearscore)
        addtime = addtime + datetime.timedelta(40)
        score = 10.0
        daymood = addDayMood(user1,addtime,score,keyword,content)
        yearscore = getMyYearScore(user1,addtime.date())
        self.failUnlessEqual(15.5,yearscore)
        yearscore = getOtherYearScore(user1,addtime.date())
        self.failUnlessEqual(0,yearscore)
class PageTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user('user1')
    def test_diary(self):
        request = self.factory.get('/diary/')
        request.user = self.user
        request.user = AnonymousUser()
        response = index(request)
        self.assertEqual(response.status_code,200)
