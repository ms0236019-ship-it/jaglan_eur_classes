from django.contrib import admin
from .models import StudentInquiry, ClassAudio, StudyPDF


@admin.register(StudentInquiry)
class StudentInquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'target_country', 'preferred_batch', 'passport_copy', 'resume_cv', 'submitted_at')
    list_filter = ('target_country', 'preferred_batch', 'submitted_at')
    search_fields = ('full_name', 'phone_number', 'email')


@admin.register(ClassAudio)
class ClassAudioAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'is_published', 'created_at')
    list_filter = ('level', 'is_published')
    search_fields = ('title', 'description')


@admin.register(StudyPDF)
class StudyPDFAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'is_published', 'created_at')
    list_filter = ('level', 'is_published')
    search_fields = ('title', 'description', 'tag')