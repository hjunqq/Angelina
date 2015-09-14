from django.conf.urls import include, url
from diary import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$','diary.views.index'),
    url(r'^login/','diary.views.login_page'),
    url(r'^logout/','diary.views.logout_page'),
    url(r'^(?P<year>\d{4})/$','diary.views.yeararchive'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$','diary.views.montharchive'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$','diary.views.dayarchive'),
]

