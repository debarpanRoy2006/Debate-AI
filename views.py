from django.shortcuts import render,HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('This is a homepage')
def about(request):
    return HttpResponse('This is about page')
def service(request):
    return HttpResponse('This is service page')
def service(request):
    return HttpResponse('This is service page')