from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Message, Comment
# from apps.app2.models import Deez
import bcrypt

def index(request):
    return render(request, "my_app/index.html")

def registration(request):
    return render(request, "my_app/registration.html")

def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/registration")
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        print(pw_hash)
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
        if user:
            request.session['new_user_id']=user.id
            return redirect("/welcome")

def welcome(request):
    if 'new_user_id' not in request.session:
        return redirect("/")
    context = {
        "user": User.objects.get(id=request.session['new_user_id']),
    }
    return render(request, "my_app/welcome.html", context)

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid']=logged_user.id
            return redirect("/loggedin")
    return redirect("/")

def logout(request):
    del request.session['userid']
    return redirect("/")

def loggedin(request):
    if 'userid' not in request.session:
        return redirect("/")
    print(request.session['userid'])
    context = {
        "user": User.objects.get(id=request.session['userid'])
    }
    return render(request, "my_app/loggedin.html", context)

def wall(request):
    context = {
        "user": User.objects.get(id=request.session['userid']),
        "messages": Message.objects.all(),
        "comments": Comment.objects.all(),
    }
    return render(request, "my_app/wall.html", context)

def postMessage(request):
    if 'userid' not in request.session:
        return redirect("/")
    message = Message.objects.create(message=request.POST["message"], user=User.objects.get(id=request.session['userid']))
    print(message.message)
    return redirect("/wall")

def postComment(request, number):
    if 'userid' not in request.session:
        return redirect("/")
    comment = Comment.objects.create(comment=request.POST["comment"], message=Message.objects.get(id=number), user=User.objects.get(id=request.session['userid']))    
    print(comment.comment)
    return redirect("/wall")