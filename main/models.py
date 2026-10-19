from django.db import models
from django.core.validators import FileExtensionValidator


class StudentInquiry(models.Model):
    COUNTRY_CHOICES = [
        ('Germany', 'Germany 🇩🇪'),
        ('Malta', 'Malta 🇲🇹'),
        ('Poland', 'Poland 🇵🇱'),
        ('France', 'France 🇫🇷'),
        ('Schengen Tourist', 'Schengen Tourist 🇪🇺'),
    ]

    BATCH_CHOICES = [
        ('Online Weekdays', 'Online (Mon–Fri)'),
        ('Sunday Offline', 'Sunday Offline Center'),
    ]

    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    target_country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, default='Germany')
    preferred_batch = models.CharField(max_length=50, choices=BATCH_CHOICES, default='Online Weekdays')

    passport_copy = models.FileField(upload_to='passports/', blank=True, null=True)
    resume_cv = models.FileField(upload_to='resumes/', blank=True, null=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.target_country} ({self.preferred_batch})"


class ClassVideo(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=300, blank=True)
    video_file = models.FileField(upload_to="videos/")
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


LEVELS = [("A1", "A1"), ("A2", "A2"), ("B1", "B1"), ("B2", "B2"), ("Visa", "Visa")]


class ClassAudio(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=300, blank=True)
    level = models.CharField(max_length=4, choices=LEVELS, default="A1")
    audio_file = models.FileField(
        upload_to="audio/",
        validators=[FileExtensionValidator(["mp3", "m4a", "wav", "ogg"])],
    )
    transcript = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["level", "-created_at"]

    def __str__(self):
        return f"{self.level} - {self.title}"


class StudyPDF(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=300, blank=True)
    tag = models.CharField(max_length=60, blank=True, help_text="e.g. Goethe-Zertifikat B1")
    level = models.CharField(max_length=4, choices=LEVELS, default="A1")
    pdf_file = models.FileField(
        upload_to="pdfs/",
        validators=[FileExtensionValidator(["pdf"])],
    )
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["level", "-created_at"]

    def __str__(self):
        return f"{self.level} - {self.title}"