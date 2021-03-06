from django.conf.urls import url
from rango import views
from django.conf import settings


# app_name = 'rango'
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$',
        views.show_category, name = 'show_category'),
    # url(r'^register/$', views.register, name='register'),
    # url(r'^login/$', views.user_login, name='login'),
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'search/', views.search, name='search'),
    url(r'goto/', views.track_url, name='goto'),
    url(r'^like_category/$', views.like_category, name='like_category'),
    url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),
    # url(r'^logout/$', views.user_logout, name='logout'),
]

#
# if settings.DEBUG:
#     urlpatterns += patterns(
#         'django.views.static',
#         (r'^media/(?P<path>.*)'),
#         'serve',
#         {'document_root':settings.MEDIA_ROOT},
#     )