from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Twix
from .forms import TwixForm


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        # Get the profiles that the current user is following
        form = TwixForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                twix = form.save(commit=False)
                twix.user = request.user
                form.save()
                messages.success(request, "Your twix has been posted!")
                return redirect("home")

        following_profiles = request.user.profile.follows.all()

        # Get Twixes from the users that the current user is following
        twixes = Twix.objects.filter(user__profile__in=following_profiles)
        return render(request, 'home.html', {"twixes": twixes, "form": form})

    else:
        twixes = Twix.objects.order_by("-creation_date")
        return render(request, 'home.html', {"twixes": twixes})


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {'profiles': profiles})
    else:
        messages.success(request, "You must be logged in to overview profile list.")
        return redirect('home.html')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)

        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']

            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)
            current_user_profile.save()

        return render(request, 'profile.html', {'profile': profile})
    else:
        messages.success(request, "You must be logged in to overview profile list.")
        return redirect('home.html')
