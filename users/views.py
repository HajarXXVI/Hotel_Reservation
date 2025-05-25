from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings

# Create your views here.

@login_required
def profile(request):
    if request.method == 'POST':
        # Update user profile
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.phone_number = request.POST.get('phone_number', '')
        user.address = request.POST.get('address', '')
        user.city = request.POST.get('city', '')
        user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('users:profile')
    
    context = {
        'moroccan_cities': settings.MOROCCAN_CITIES
    }
    return render(request, 'users/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Add profile edit logic here
        messages.success(request, _('Profile updated successfully!'))
        return redirect('users:profile')
    return render(request, 'users/edit_profile.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your password was successfully updated!'))
            return redirect('users:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})

@login_required
def user_reservations(request):
    return redirect('reservations:reservation_list')
