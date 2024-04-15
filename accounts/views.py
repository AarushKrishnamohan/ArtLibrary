from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import make_password
# Create your views here.


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        #authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"type": "success", "message": "Your have been logged in successfully."})
        else:
            return JsonResponse({"type": "Error", "message": "Invalid Password or Username"})

    return render(request, 'accounts/login.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        user = User.objects.filter(username=username)
        if user:
            return JsonResponse({"type": "Error", "message": "Another account with this username already exists"})
        if password != confirm_password:
            return JsonResponse({"type": "Error", "message": "Your Password Fields Don't Match"})
        
        new_user = User.objects.create_user(username, email, password)


        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()
        return JsonResponse({"type": "Success", "message": "Your Account has been Created"})
    


    return render(request, 'accounts/signup.html')

def logout_user(request):
    logout(request)
    return redirect('login')

def reset_password(request):
    return render(request, 'accounts/resetpass.html')

def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        #check password correct
        if not request.user.check_password(old_password):
            return JsonResponse({"type": 'error', "message": "Your old password is not correct"})
        
        #check new password
        if new_password != confirm_new_password:
            return JsonResponse({"type": "error", "message": "Passwords do not match"})
        
        request.user.password = make_password(new_password)
        request.user.save()

        update_session_auth_hash(request, request.user)

        return JsonResponse({"type": "success", "message": "Your password has been updated successfully"})
        


    return render(request, 'accounts/changepass.html')

def reset_change_password(request):
    return render(request, 'accounts/changepass.html')
def reset_password_confirmation(request):
    return render(request, 'accounts/resetpasssucess.html')

