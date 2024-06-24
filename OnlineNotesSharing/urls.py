"""OnlineNotesSharing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from notes.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    path('admin/', admin.site.urls),


    path('',index,name='index'),    
    path('login',user_login,name='login'),        
    path('register',register,name='register'),

    
    path('user_profile',user_profile,name='user_profile'),
    path('edit_profile',edit_profile,name='edit_profile'),
    path('change_password',change_password,name='change_password'),
    path('view_all_notes',view_all_notes,name='view_all_notes'),    
    path('upload_notes',upload_notes,name='upload_notes'),
    path('view_mynotes',view_mynotes,name='view_mynotes'),
    path('delete_mynotes/<int:uid>',delete_mynotes,name='delete_mynotes'),
    path('edit_mynotes/<int:eid>',edit_mynotes,name='edit_mynotes'),
    

    
    path('login_admin',login_admin,name='login_admin'),
    path('admin_home',admin_home,name='admin_home'),
    path('view_users',view_users,name='view_users'),
    path('delete_users/<int:uid>',delete_users,name='delete_users'),
    path('panding_notes',panding_notes,name='panding_notes'),
    path('assign_status/<int:aid>',assign_status,name='assign_status'),
    path('accepted_notes',accepted_notes,name='accepted_notes'),
    path('rejected_notes',rejected_notes,name='rejected_notes'),
    path('all_notes',all_notes,name='all_notes'),
    path('delete_notes/<int:uid>',delete_notes,name='delete_notes'),

    path('logout',Logout,name='logout'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
