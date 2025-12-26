from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name




class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    original_image = models.ImageField(upload_to='scans/')
    ocr_text = models.TextField(blank=True)
    subject = models.CharField(max_length=100, blank=True)  
    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True)
    summary = models.TextField(blank=True)
    study_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title


class Flashcard(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="flashcards")
    question = models.TextField()
    answer = models.TextField()