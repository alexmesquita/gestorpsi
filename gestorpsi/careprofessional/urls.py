from django.conf.urls.defaults import *

urlpatterns = patterns('gestorpsi.careprofessional.views',
    (r'^$', 'index'),
    (r'^add/$', 'form'),
    (r'^(?P<object_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', 'form'),    
)