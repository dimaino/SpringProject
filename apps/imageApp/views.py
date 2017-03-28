from django.shortcuts import render, HttpResponse, redirect
from .forms import ImageUploadForm
from .models import ImageModel



def index(request):
    return render(request, "imageApp/index.html")

def uploadImage(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = ImageModel()
            m.model_pic = form.cleaned_data['image']
            m.save()
            return redirect('spring:showImage')
        return HttpResponse('NOOOOOOOOOOOOOOOOOOOOOOO')


def allImages(request):
    something = ImageModel.objects.all()
    print something
    context = {
        'yall':something
    }
    return render(request, "imageApp/index2.html", context)
