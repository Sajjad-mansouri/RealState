from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth,messages
from contacts.models import Contact

def register(request):
    if request.method== 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1==password2:

            if User.objects.filter(username=username).exists():
                messages.error(request,'username taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'email taken')
                    return redirect('register')
                else:
                    user=User.objects.create_user(username=username,password=password1,email=email,
                    first_name=first_name,last_name=last_name
                    )
                    #login after registration
                    user.save()
                    auth.login(request,user)
                    messages.success(request,'you are regestered and can login ')
                    return redirect('index')
                    # user.save()
                    # messages.success(request,'you are regestered and can login ')
                    # return redirect('login')
        else:

                messages.error(request,"passwords don't match")
                return redirect('register')



    else:
        return render(request,'accounts/register.html')

def login(request):
    if request.method== 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'you successfully loged in')
            return redirect('dashboard')
        else:
            messages.error(request,'credential is not valid')
            return redirect('login')
    else:
        return render(request,'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'you successfully loged out')
        return redirect('index')



def dashboard(request):
    user_id=request.user.id
    user_contact=Contact.objects.order_by('-contact_date').filter(user_id=user_id)
    context={'contacts':user_contact}
    return render(request,'accounts/dashboard.html',context)
