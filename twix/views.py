from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Twix
from .forms import TwixForm, RegisterForm, ProfileImgForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django import forms


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
        twixes = Twix.objects.filter(user_id=pk)

        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']

            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)
            current_user_profile.save()

        return render(request, 'profile.html', {'profile': profile, 'twixes': twixes})
    else:
        messages.success(request, "You must be logged in to overview profile list.")
        return redirect('home.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully login!")
            return redirect('home')
        else:
            messages.success(request, "Invalid authentication credentials")
            return redirect('login')
    return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully logout!")
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            # first_name = form.cleaned_data["first_name"]
            # last_name = form.cleaned_data["last_name"]
            # email = form.cleaned_data["email"]

            # Log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully register!")
            return redirect('home')
    return render(request, "register.html", {})


def update_user(request):
    if request.user.is_authenticated:

        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)

        user_form = RegisterForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfileImgForm(request.POST or None, request.FILES or None, instance=profile_user)

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, "Your profile has been successfully updated!")
            return redirect('home')

        return render(request, "update_user.html", {"user_form": user_form, "profile_form": profile_form})
    else:
        messages.success(request, "You must me logged in for that action!")
        return redirect('home')

