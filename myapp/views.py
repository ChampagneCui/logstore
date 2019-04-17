from django.shortcuts import render
from myapp.utils.sts import return_sts

# Create your views here.
def logstore(request):
    url=return_sts()
    return render(request,'index.html',{"url": url})
