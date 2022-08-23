from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from listings.models import Listing

from .models import Contact
def contact(request):
    if request.method == 'POST':
        listing_id=request.POST['listing_id']
        listing=request.POST['listing']
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        message=request.POST['message']
        user_id=request.POST['user_id']
        realtor_email=request.POST['realtor_email']
        realtor=Listing.objects.get(title=listing).realtor


        #check if user has made inquiry already
        if request.user.is_authenticated:
            #user_id=request.user.id
            has_contacted=Contact.objects.all().filter(listing_id=listing_id,user_id=user_id)
            if has_contacted:
                messages.error(request,'you have already made an inquiry for this  listing')
                return redirect('/listings/'+listing_id)


        contact=Contact(listing_id=listing_id,listing=listing,name=name,
        email=email,phone=phone,message=message,user_id=user_id
        )
        contact.save()
        #send Email
        subject='Property Listing Inquiry'
        message=f'Hi {realtor}\tthere has been an inquiry for '+listing+'.sign in to admin panel for more info'
        from_mail=settings.EMAIL_HOST_USER
        to_email=[realtor_email,]
        send_mail(
                subject,
                message,
                from_mail,
                to_email,
                fail_silently=False,
            )

        messages.success(request,'your request has submitted ,realtor get back to you soon')
        return redirect('/listings/'+listing_id)
