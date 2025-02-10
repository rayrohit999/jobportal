from django.shortcuts import render

# Create your views here.
def home(request):
    context={
        'name':'Rahul Gupta',
        'content':'CareerHub helped me land my dream job in just two weeks! Highly recommended!'
    }
    return render(request,'home/index.html',context)