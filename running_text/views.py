import os

from django.contrib import messages
from django.shortcuts import render
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from .create_running_text_video import create_running_text_video
from django.views.decorators.csrf import csrf_exempt

from .models import Runtext
from .forms import RuntextForm


def run_text(request):
    text = request.GET.get("text", "")
    if text.strip() == "":
        return HttpResponse("<h1>Для создания видео введите текст в параметр \"text\" адресной строки!</h1>")
    Runtext.objects.create(text=text)
    create_running_text_video(text)
    with open("video.mp4", 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="video/quicktime")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename("video.mp4")
        return response

    # return FileResponse(open("video.mp4", "rb"), as_attachment=True)


@csrf_exempt
def index(request):
    if request.method == "POST":
        form = RuntextForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            form.save()
            create_running_text_video(
                text=cleaned_data["text"],
                width=cleaned_data["width"],
                height=cleaned_data["height"],
                duration=cleaned_data["duration"],
                text_color=cleaned_data["text_color"],
                background_color=cleaned_data["background_color"],
                font_size=cleaned_data["font_size"],
            )
            with open("video.mp4", 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="video/quicktime")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename("video.mp4")
                return response
            # return FileResponse(open("video.mp4", "rb"), content_type="video/mp4", as_attachment=True)
    else:
        form = RuntextForm()
    return render(request, "running_text/index.html", {"form": form})
