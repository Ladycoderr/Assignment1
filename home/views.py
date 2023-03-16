from django.db.models.fields import EmailField
from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from .models import Person, Company


# Render the home page
def index(request):
    return render(request,'index.html')


# Handle user login
def loginuser(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method=='POST':
            email= request.POST.get('email')
            password = request.POST.get('password')
            # Check if user with given email exists in Person table
            user = Person.objects.filter(email=email)
            user = list(user)
            if len(user) != 0:
                # If user exists, authenticate using email as username and given password
                user = authenticate(username=user[0].username, password=password)
            else:
                user = None
            if user is not None:
                 # If authentication successful, log user in and redirect to home page
                login(request,user)
                return redirect('/')
            else:
                # If authentication failed, show error message and redirect to login page
                messages.error(request,'username or password not correct')
                return redirect('login')
        # Render the login page if request method is GET
        return render(request,'login.html')


# Handle user registration
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        fullname = request.POST.get('fullname')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
      
# Check if email already exists in Person table
        if Person.objects.filter(email=email).exists():
            mess ={'abcd':'EMAIL ALREADY  EXIST'}
            return render(request,'login.html',mess)
 # Check if username already exists in User table
        elif User.objects.filter(username=username).exists():
            mess ={'abcd':'USERNAME ALREADY  EXIST'}
            return render(request,'login.html',mess)

        else:
            # Create new Person and User objects with given details
            per = Person(username=username, email=email,Phone=phone, address=address, fullname=fullname)
            per.save()
            user = User.objects.create_user(username=username, password=password)
            user.save()
            # Authenticate and log user in
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                # If authentication failed, show error message and redirect to login page
                messages.error(request,'username or password not correct')
                return redirect('/login')
    # Redirect to login page if request method is not POST
    return redirect('login')


# Handle company registration
def register_company(request):
    if request.user.is_authenticated == False:
        return redirect('/')
    else :
        if request.method == 'POST':
            company = request.POST.get('name')
            about = request.POST.get('about')
            address = request.POST.get('address')
            username = request.user.username
             # Check if company already registered with given email
            if Company.objects.filter(email = username).exists():
                messages.error(request,'company name is already registered')
                return redirect('/company_detail')
            else:
                # Create new Company object with given details
                comp = Company(name = company, about = about, address = address, email = username)
                comp.save()
                messages.success(request, "Company Registered Successfully")
                return redirect('/company_detail')
# Render the company registration page if request method is GET
    return render(request, "company_register.html" , {}) 

#showing user details
def user_detail(request):
    if request.method == 'POST':
        #if request method is post updating the details
        user = Person.objects.filter(username= request.user.username)[0]
        user.fullname = request.POST.get('fullname')
        user.address = request.POST.get('address')
        user.Phone = request.POST.get('Phone')
        user.save()
        #after successfully updation redirecting to the same page
        return redirect('/user_detail')
        #if request method is get and the user not logged in redirecting to the login page
    elif request.user.is_authenticated == False:
        return redirect("/login")
        #if request method is get and the user is logged in we'll show user details
    else:
        user = Person.objects.filter(username= request.user).values()
        
        return render(request,"user_details.html", {'user' : user[0]})



def company_detail(request):
    if request.method == 'POST':
        # Retrieves the logged-in company's details and updates them with the POST data
        company = Company.objects.filter(email= request.user.username)[0]
        print(company)
        print(request.POST)
        company.name = request.POST.get('name')
        company.about = request.POST.get('about')
        company.address = request.POST.get('address')
        company.save()
        # Redirects the user to the company details page
        return redirect('/company_detail')
        # Redirects the user to the login page if they are not logged in
    elif request.user.is_authenticated == False:
        return redirect("login")
        # Redirects the user to the company registration page if they have not yet registered
    elif Company.objects.filter(email = request.user.username).exists() == False:
        return redirect('/company_register')
        # Retrieves and displays the logged-in company's details
    else:
        company = Company.objects.filter(email= request.user.username).values()
        return render(request,"company_details.html", {'company' : company[0]})

#function logs out the user and redirects them to the home page
def logoutuser(request):
    logout(request)
    return redirect('index')

#function deletes the logged-in user and from the database and also deletes the company associated with him
# and redirects to the login page
def delete_user(request):
    username = request.user.username
    logout(request)
    user = Person.objects.filter(username= username)[0]
    if Company.objects.filter(email = username).exists() == True:
        company = Company.objects.filter(email= username)[0]
        company.delete()
    user.delete()
    u = User.objects.get(username = username)
    u.delete()
# Redirects the user to the login page
    return redirect("/login")

# function deletes the logged-in company from the database and redirects to the company registration page
def delete_company(request):
    company = Company.objects.filter(email= request.user.username)[0]
    company.delete()
    return redirect("/company_register")
