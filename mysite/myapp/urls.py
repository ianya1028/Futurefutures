from django.conf.urls import url

from . import views
#from django.urls import path

urlpatterns = [
    url(r'^$',views.app_list),
    url(r'^(?P<slug>[/w-]+)/$',views.app_detail),
]
