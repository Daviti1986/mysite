from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^panel/manager/list/$', views.manager_list, name = 'manager_list'),
    url(r'^panel/manager/delete/(?P<pk>\d+)/$', views.manager_delete, name = 'manager_delete'),
    url(r'^panel/manager/group/$', views.manager_group, name = 'manager_group'),
    url(r'^panel/manager/perms/$', views.manager_permissions, name = 'manager_permissions'),
    url(r'^panel/manager/group/add/$', views.manager_group_add, name = 'manager_group_add'),
    url(r'^panel/manager/group/delete/(?P<name>.*)/$', views.manager_group_delete, name = 'manager_group_delete'),
    url(r'^panel/manager/group/show/(?P<pk>\d+)/$', views.users_group, name = 'users_group'),
    url(r'^panel/manager/addgroup/(?P<pk>\d+)/$', views.add_users_to_group, name = 'add_users_to_group'),
    url(r'^panel/manager/perms/show/(?P<pk>\d+)/$', views.users_permissions, name = 'users_permissions'),
    url(r'^panel/manager/delgroup/(?P<pk>\d+)/(?P<name>.*)/$', views.delete_users_to_group, name = 'delete_users_to_group'),
    url(r'^panel/manager/perms/delete/(?P<name>.*)/$', views.manager_permissions_delete, name = 'manager_permissions_delete'),
    url(r'^panel/manager/perms/add/$', views.manager_permissions_add, name = 'manager_permissions_add'),
    url(r'^panel/manager/delperm/(?P<pk>\d+)/(?P<name>.*)/$', views.users_permissions_delete, name = 'users_permissions_delete'),
    url(r'^panel/manager/addperm/(?P<pk>\d+)/$', views.users_permissions_add, name = 'users_permissions_add'),
    url(r'^panel/manager/addpermtogroup/(?P<name>.*)/$', views.groups_permissions, name = 'groups_permissions'),
    url(r'^panel/manager/group/delperms/(?P<group_name>.*)/(?P<name>.*)/$', views.groups_permissions_delete,
        name = 'groups_permissions_delete'),
    url(r'^panel/manager/addperms/(?P<name>.*)/$', views.groups_permissions_add, name = 'groups_permissions_add'),
]