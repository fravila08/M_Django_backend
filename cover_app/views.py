from django.shortcuts import render

# Create your views here.
def send_home(request):
    return render(request, "index.html")