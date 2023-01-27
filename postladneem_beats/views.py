from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import FileResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.utils.datastructures import MultiValueDictKeyError

from postladneem_beats.models import Beat, Genre, Key


def download_action(request):
    if not request.user:
        redirect("/login/")
    beat_to_download = get_object_or_404(Beat, pk=request.GET["id"])
    response = FileResponse(
        beat_to_download.file.file, filename=beat_to_download.file.name, content_type="audio/mpeg", as_attachment=True
    )
    return response


def remove_action(request):
    if not request.user:
        redirect("/login/")
    if not Beat.objects.filter(pk=request.GET["id"]).exists():
        return redirect("/feed/")
    beat_to_delete = Beat.objects.get(pk=request.GET["id"])
    if request.user.is_superuser or request.user in beat_to_delete.authors.all():
        beat_to_delete.delete()
    return redirect("/feed/")


def edit_action(request):
    if not request.user:
        redirect("/login/")

    if not request.GET.get("id"):
        return HttpResponseBadRequest("No ID provided")

    if request.method == "POST":
        beat_to_edit = get_object_or_404(Beat, pk=request.GET["id"])
        if request.POST["name"] != beat_to_edit.name and Beat.objects.filter(name=request.POST["name"]).exists():
            raise ValidationError("Имя уже занято")

        beat_to_edit.description = request.POST["description"]
        beat_to_edit.genre = Genre.objects.get(pk=request.POST["genre"])
        beat_to_edit.key = Key.objects.get(pk=request.POST["key"])
        beat_to_edit.bpm = int(request.POST["bpm"])
        beat_to_edit.save()

    return redirect("/mine/")


def registration_page(request):
    return render(request, "registration.html")


def edit_page(request):
    if not request.user:
        redirect("/login/")
    if not request.GET.get("id"):
        return HttpResponseBadRequest("No ID provided")
    if request.method == "GET":
        beat_to_edit = get_object_or_404(Beat, pk=request.GET["id"])
        return render(
            request,
            "edit.html",
            context={
                "beat": beat_to_edit,
                "genres": Genre.objects.all(),
                "keys": Key.objects.all(),
            },
        )


def registration_action(request):
    if not request.user:
        redirect("/login/")
    username = request.POST["username"]
    approval = request.POST["approval"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request=request, user=user)
        return redirect("/feed/")
    else:
        if approval == password:
            login(request=request, user=User.objects.create_user(username=username, password=password))
            return redirect("/feed/")
        else:
            return HttpResponseBadRequest()


def logout_action(request):
    logout(request)
    return redirect("/login/")


def login_action(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request=request, user=user)
        return redirect("/feed/")
    else:
        return HttpResponseForbidden("Invalid credentials")


def root_page(request):
    if not request.user:
        return redirect("/login/", permanent=True)
    return redirect("/feed/", permanent=True)


def login_page(request):
    return render(request, "login.html")


def feed_page(request):
    if not request.user:
        redirect("/login/")
    context = {
        "beats": Beat.objects.order_by("name"),
    }
    return render(request, "feed.html", context)


def creation_page(request):
    user = request.user
    keys = Key.objects.all()
    genres = Genre.objects.all()
    template = loader.get_template("creation.html")
    context = {
        "user": user,
        "keys": keys,
        "genres": genres,
    }
    return HttpResponse(template.render(context, request))


def create_beat_action(request):
    if request.method == "POST":
        try:
            new_beat = Beat(
                name=request.POST["name"],
                description=request.POST["description"],
                genre=Genre.objects.get(name=request.POST["genre"]),
                bpm=int(request.POST["bpm"]),
                key=Key.objects.get(tonica=request.POST["key"][0], is_minor="m" in request.POST["key"]),
            )
            new_beat.file.save(request.FILES["file"].name, request.FILES["file"])
        except:
            return HttpResponseBadRequest()

        new_beat.authors.set([request.user])
        new_beat.save()
        return redirect("/feed/")
    return HttpResponse(status=405)


def mine_page(request):
    context = {
        "beats": Beat.objects.filter(authors__pk__exact=request.user.pk).order_by("name"),
    }
    return render(request, "feed.html", context)
