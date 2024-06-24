from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate,login,logout
from datetime import date
import os

# Create your views here.

# index pages start

def index(request):
    return render (request,'index.html')


def register(request):
    error = ""
    if request.method=='POST':
        f = request.POST['firstname']
        l = request.POST['lastname']
        c = request.POST['contact']
        e = request.POST['emailid']
        p = request.POST['password']
        b = request.POST['branch']
        r = request.POST['role']
        try:
            if User.objects.filter(email=e).exists():       
                error='yes'     
            else:
                user = User.objects.create_user(username=e,password=p,first_name=f,last_name=l)
                Signup.objects.create(user=user,contact=c,branch=b,role=r)
                error='no'
        except:
            error='ha'
    d={'error':error}        
    return render (request,'register.html',d)


def user_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['emailid']
        p = request.POST['pwd']
        user = authenticate (username=u,password=p)
        try:
            if user:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"   
    
    return render (request,'login.html',locals())

# index pages end

#-------------------------------------------------------------

# user pages start

def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    data = Signup.objects.get(user = user)
    d = {'data':data,'user':user}
    return render (request,'user_profile.html',d)

def change_password(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    if request.method=="POST":
        o = request.POST['o_pass']
        n = request.POST['n_pass']
        c = request.POST['c_pass']  
        if c==n:             
            u = User.objects.get(username__exact = request.user.username)
            u.set_password(n)
            u.save()  
            error="no"
        else:
            error="yes"
    d = {
        'error':error
    }
    return render (request,'change_password.html',d)

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    user = User.objects.get(id=request.user.id)
    data = Signup.objects.get(user = user)
    error="False"
    if request.method=="POST":
        f =request.POST['f_name']
        l =request.POST['l_name']        
        c =request.POST['c_no']
        b =request.POST['branch']
        r =request.POST['role']

        user.first_name = f
        user.last_name = l
        data.contact = c
        data.branch = b
        data.role = r

        user.save()
        data.save()
        error = "True"

    d = {'data':data,'user':user,'error':error}
    return render (request,'edit_profile.html',d)

    

def upload_notes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    if request.method=="POST":
        br =request.POST['branch']
        su =request.POST['Subject']        
        nf =request.FILES['n_file']
        ft =request.POST['f_type']
        de =request.POST['description']
        u = User.objects.filter(username=request.user.username).first()
        try:
            note = Notes.objects.create(user=u,uploadingdate=date.today(),branch=br,subject=su,notesfile=nf,filetype=ft,description=de,
            status='pending')
            error="no"
        except:
            error="yes"

    return render (request,'upload_notes.html',locals())


def view_mynotes(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = User.objects.get(id=request.user.id)
    notes = Notes.objects.filter(user = user)
    accept = Notes.objects.filter(status = "pending")
    s = notes.count()

    d = {
        'notes':notes , 'accept':accept ,'s':s
    }
    return render(request,'view_mynotes.html',d)

def view_all_notes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.all()
    all_notes = Notes.objects.filter(status = "Accept")
    asum = all_notes.count()
    d = {
        'all_notes':all_notes , 'user':user ,'asum':asum
    }
    return render (request,'view_all_notes.html',d)


def delete_mynotes(request,uid):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.get(id=uid)
    notes.delete()
    return redirect('view_mynotes')

def edit_mynotes(request,eid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.get(id=eid)
    error=""
    if request.method=="POST": 
        if len(request.FILES)!=0:
            if len(notes.notesfile) > 0:
                os.remove(notes.notesfile.path)
            notes.notesfile = request.FILES['n_file']
        try:
            notes.subject = request.POST.get('Subject')       
            notes.branch =request.POST.get('branch')         
            notes.filetype = request.POST.get('f_type')
            notes.description = request.POST.get('description')
            notes.save()
            error="no"           
        except:
            error="yes"      
    d = {
        'notes':notes,'error':error
    }
    return render (request,'edit_mynotes.html',d)

def show_files(request0):
    filepath = os.path.join('static','sample')

# user pages end

#-------------------------------------------------------------

# admin pages start

def login_admin(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate (username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"
    
    return render (request,'login_admin.html',locals())
    
def admin_home(request):
    if not request.user.is_staff:
        return redirect('login_admin')
    p = Notes.objects.filter(status="pending").count()
    a = Notes.objects.filter(status="Accept").count()
    r = Notes.objects.filter(status="Reject").count()
    all = Notes.objects.all().count()

    prp = p / 100
    pra = a / 100
    prr = r / 100
    prall = all / 100

    d = {

        'p':p, 'a':a, 'r':r, 'all':all , 'prp':prp, 'pra':pra, 'prr':prr, 'prall':prall 
    }

    return render (request,'admin_home.html',d)


def view_users(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    users = Signup.objects.all()  

    d = {
        'users':users
    }
    return render (request,'view_users.html',d)

def delete_users(request,uid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    users = User.objects.get(id=uid)
    users.delete()
    return redirect('view_users')


def panding_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    p_notes = Notes.objects.filter(status = "pending")
    d = {
        'p_notes':p_notes
    }
    return render (request,'panding_notes.html',d)

def accepted_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    a_notes = Notes.objects.filter(status = "Accept")
    d = {
        'a_notes':a_notes
    }
    return render (request,'accepted_notes.html',d)

def rejected_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    r_notes = Notes.objects.filter(status = "Reject")
    d = {
        'r_notes':r_notes
    }
    return render (request,'rejected_notes.html',d)


def all_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    all_notes = Notes.objects.all()
    d = {
        'all_notes':all_notes
    }
    return render (request,'all_notes.html',d)

def delete_notes(request,uid):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.get(id=uid)
    notes.delete()
    return redirect('all_notes')


def assign_status(request,aid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.get(id=aid)
    error=""
    if request.method=="POST":        
        s =request.POST['status'] 
        try:
            notes.status = s
            notes.save()
            error="no"
        except:
            error="yes"      
    d = {
        'notes':notes,'error':error
    }
    return render (request,'assign_status.html',d)

# admin pages end

#-------------------------------------------------------------

# logout page start

def Logout(request):
    logout(request)
    return redirect ('index')

# logout page end

#-------------------------------------------------------------

