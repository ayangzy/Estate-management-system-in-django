from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact

# Create your views here.


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # check if user has already made an inquiry
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(
                listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(
                    request, 'You have already made an enquiry for this listing')
                return redirect('/listings/' + listing_id)

        # save user listing contact to database
        contact = Contact(listing_id=listing_id,
                          listing=listing, name=name, email=email, phone=phone, message=message, user_id=user_id)
        contact.save()

        # send email
        send_mail(
            'Property listing inquiry',
            'There has been an inquiry for ' + listing +
            '. Sign into the admin panel for more info',
            'ayangefelix8@gmail.com',
            [realtor_email, 'logicfatee360@gmail.com'],
            fail_silently=False
        )

        messages.success(
            request, 'Your request has been submitted, a realtor will get back to you soon')
        return redirect('/listings/' + listing_id)
