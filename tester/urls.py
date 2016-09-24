from django.conf.urls import url

from . import views


app_name = 'tester'

urlpatterns = [
    # /tester/
    url(r'^$', views.index, name='index'),
    # /tester/result
    url(r'^result/$', views.result, name='result'),
    # /tester/5/
    url(r'^(?P<feature_id>[0-9]+)/$', views.detail, name='detail'),
    # /tester/5/detailresult
    url(r'^(?P<feature_id>[0-9]+)/detailresult/$', views.detailresult, name='detailresult'),
    # /tester/5/2/
    url(r'^(?P<feature_id>[0-9]+)/(?P<scenario_id>[0-9]+)/$', views.detailscenario, name='detailscenario'),
    # /tester/5/detailscenarioresult
    url(r'^(?P<scenario_id>[0-9]+)/detailscenarioresult/$', views.detailscenarioresult, name='detailscenarioresult'),
]