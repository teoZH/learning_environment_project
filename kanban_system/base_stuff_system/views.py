from django.shortcuts import render, redirect


# Create your views here.


def homepage(request):
    if not request.user.is_authenticated:
        return render(request, 'homepage.html')
    return redirect('profile_page', request.user.pk)
