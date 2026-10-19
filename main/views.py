import os
import re

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import StudentInquiry, ClassVideo

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB (passport / CV)
PASSPORT_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}
RESUME_EXTENSIONS = {".pdf", ".doc", ".docx"}
PHONE_PATTERN = re.compile(r"^[+0-9\s\-]{10,16}$")

MAX_VIDEO_SIZE = 300 * 1024 * 1024  # 300 MB
VIDEO_EXTENSIONS = {".webm", ".mp4", ".mov", ".m4v"}


def home(request):
    videos = [
        {
            "title": v.title,
            "desc": v.description,
            "file": v.video_file.url if v.video_file else "",
            "youtube": v.youtube_id,
        }
        for v in ClassVideo.objects.filter(is_published=True)
    ]
    return render(request, "index.html", {"videos": videos})


def _file_error(file, allowed_extensions, label):
    """Return an error message if the uploaded file is not acceptable, else None."""
    if not file:
        return None
    if file.size > MAX_FILE_SIZE:
        return f"{label} must be 5 MB or smaller."
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in allowed_extensions:
        return f"{label} must be one of: {', '.join(sorted(allowed_extensions))}."
    return None


def submit_inquiry(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request."}, status=405)

    full_name = request.POST.get("name", "").strip()
    phone_number = request.POST.get("phone", "").strip()
    email = request.POST.get("email", "").strip()
    target_country = request.POST.get("country")
    preferred_batch = request.POST.get("mode")

    passport = request.FILES.get("passport")
    resume = request.FILES.get("resume")

    if not full_name or not phone_number:
        return JsonResponse({"status": "error", "message": "Name and Phone number are required."}, status=400)

    if not PHONE_PATTERN.match(phone_number):
        return JsonResponse({"status": "error", "message": "Please enter a valid phone number."}, status=400)

    error = _file_error(passport, PASSPORT_EXTENSIONS, "Passport copy") or _file_error(resume, RESUME_EXTENSIONS, "Resume")
    if error:
        return JsonResponse({"status": "error", "message": error}, status=400)

    StudentInquiry.objects.create(
        full_name=full_name,
        phone_number=phone_number,
        email=email,
        target_country=target_country,
        preferred_batch=preferred_batch,
        passport_copy=passport,
        resume_cv=resume,
    )
    return JsonResponse({"status": "success", "message": "Inquiry submitted successfully!"})


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.save())
        return redirect("dashboard")
    return render(request, "auth.html", {"form": form, "title": "Create your student account"})


@login_required
def dashboard(request):
    return render(request, "dashboard.html")


# ---------- Teacher tools: record and publish lesson videos ----------

@staff_member_required
def record_lesson(request):
    return render(request, "record.html")


@require_POST
def upload_video(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({"status": "error", "message": "Only staff can upload videos."}, status=403)

    title = request.POST.get("title", "").strip()
    description = request.POST.get("description", "").strip()
    publish = request.POST.get("publish") == "on"
    video = request.FILES.get("video")

    if not title:
        return JsonResponse({"status": "error", "message": "Please add a title."}, status=400)
    if not video:
        return JsonResponse({"status": "error", "message": "No video received."}, status=400)
    if video.size > MAX_VIDEO_SIZE:
        return JsonResponse({"status": "error", "message": "Video must be 300 MB or smaller."}, status=400)
    if os.path.splitext(video.name)[1].lower() not in VIDEO_EXTENSIONS:
        return JsonResponse({"status": "error", "message": "Use a .webm, .mp4, .mov or .m4v video."}, status=400)

    ClassVideo.objects.create(
        title=title[:120],
        description=description[:300],
        video_file=video,
        is_published=publish,
    )
    return JsonResponse({"status": "success", "message": "Video saved."})