from django.shortcuts import render, get_object_or_404
from .models import Animation, Image
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from redis import Redis
import django_rq
from rq import Queue, Worker

@login_required
def index(request):
    if request.method == 'POST':
        anim = Animation.objects.create(name=request.POST['name'], user_id=request.user.id)#user_id=request.user.id
        for img in request.FILES.getlist('imgs'):
            Image.objects.create(animation=anim, image=img)

    anims = Animation.objects.filter(user=request.user)#before: objects.All()
    context = {
            'anims': anims
    }
    return render(request, 'mkgif/index.html', context)

@login_required
def details(request, pk):
    #get the specific animation
    anim = get_object_or_404(Animation, pk=pk)
    #get the images that belong to that animation
    images = Image.objects.filter(animation=pk)

    queue = Queue(connection=Redis())
    frames = Animation.objects.get(pk=pk)
    gif = frames.enqueue({})

    context = {
            'anim': anim,
            'images': images,
            'gif': gif,
            }

    return render(request, 'mkgif/details.html', context)

@login_required
def delete_animation(request, pk):
    anim = get_object_or_404(Animation, pk=pk)
    anim.delete()

    return HttpResponseRedirect(reverse('mkgif:index'))
