from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileUpdateForm
from bikes.models import Bike

@login_required
def profile_view(request):
    user_bikes = Bike.objects.filter(seller=request.user).order_by('-created_at')
    return render(request, 'users/profile.html', {
        'user': request.user,
        'user_bikes': user_bikes
    })

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile_view')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})
