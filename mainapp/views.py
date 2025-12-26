from rest_framework import viewsets, permissions, filters
from .models import Note, Subject, Tag
from .serializers import NoteSerializer, SubjectSerializer, TagSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer

from django.http import FileResponse
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound

from .services.genai import generate
from .services import prompts
import json
from .services.ocr import extract_text
from .services.pdf import generate_pdf
import traceback


MAX_CHARS = 4000  # safe for Gemini


def safe_text(text: str) -> str:
    return text[:MAX_CHARS] if text else ""

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'ocr_text', 'subject__name']

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        
        note = serializer.save(user=self.request.user)
        note.ocr_text = extract_text(note.original_image.path)
        note.pdf_file = generate_pdf(note)
        note.save()

    def perform_update(self, serializer):
        note = serializer.save()
        note.pdf_file = generate_pdf(note)
        note.save()

    @action(detail=True, methods=['get'])
    def pdf(self, request, pk=None):
        note = self.get_object()
        print(note.pdf_file)
        if not note.pdf_file:
            raise NotFound("PDF not available")

        return FileResponse(
            open(note.pdf_file.path, 'rb'),
            as_attachment=True,
            filename=f"{note.title}.pdf"
        )

    @action(detail=True, methods=["post"])
    def ai_format(self, request, pk=None):
        note = self.get_object()
        formatted = generate(prompts.format_notes(note.ocr_text))
        note.ocr_text = formatted
        note.pdf_file = generate_pdf(note)
        note.save()
        return Response({"ocr_text": formatted})

    @action(detail=True, methods=["post"])
    def detect_subject(self, request, pk=None):
        note = self.get_object()

        subject = generate(
            prompts.subject_prompt(note.ocr_text)
        )

        note.subject = subject
        note.save()

        return Response({"subject": subject})

    @action(detail=True, methods=["post"])
    def generate_summary(self, request, pk=None):
        note = self.get_object()

        summary = generate(
            prompts.summary_prompt(note.ocr_text)
        )

        note.summary = summary
        note.save()

        return Response({"summary": summary})
    @action(detail=True, methods=["post"])
    def generate_flashcards(self, request, pk=None):
        note = self.get_object()

        raw = generate(
            prompts.flashcards_prompt(note.ocr_text)
        )

        try:
            flashcards = json.loads(raw)
        except json.JSONDecodeError:
            return Response(
                {"error": "Invalid AI response"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        note.study_data = {"flashcards": flashcards}
        note.save()

        return Response({"flashcards": flashcards})


    @action(detail=True, methods=["post"])
    def generate_study(self, request, pk=None):
        try:
            note = self.get_object()
            text = safe_text(note.ocr_text)

            # --------------------
            # SUBJECT
            # --------------------
            try:
                subject = generate(prompts.subject_prompt(text))
            except Exception as e:
                print("❌ SUBJECT FAILED:", e)
                subject = ""

            # --------------------
            # SUMMARY
            # --------------------
            try:
                summary = generate(prompts.summary_prompt(text))
            except Exception as e:
                print("❌ SUMMARY FAILED:", e)
                summary = ""

            # --------------------
            # FLASHCARDS (OPTIONAL)
            # --------------------
            flashcards = []
            try:
                raw_flashcards = generate(prompts.flashcards_prompt(text))

                print("RAW FLASHCARDS RESPONSE 👇")
                print(raw_flashcards)

                # Gemini sometimes returns text before JSON
                json_start = raw_flashcards.find("[")
                json_end = raw_flashcards.rfind("]") + 1

                if json_start != -1 and json_end != -1:
                    flashcards = json.loads(raw_flashcards[json_start:json_end])
                else:
                    print("⚠️ Flashcards JSON not found")

            except Exception as e:
                print("⚠️ FLASHCARDS FAILED:", e)

            return Response({
                "subject": subject.strip(),
                "summary": summary.strip(),
                "flashcards": flashcards,
            })

        except Exception as e:
            print("🔥 GENERATE STUDY FATAL ERROR")
            traceback.print_exc()
            return Response(
                {"error": "Failed to generate study material"},
                status=500
            )



class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subject.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=201)
        return Response(serializer.errors, status=400)
