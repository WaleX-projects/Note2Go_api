from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet, SubjectViewSet, TagViewSet,RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = DefaultRouter()
router.register('notes', NoteViewSet, basename='note')
router.register('subjects', SubjectViewSet,basename='subject')
router.register('tags', TagViewSet,basename='tags')

urlpatterns = router.urls


urlpatterns += [
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='register'),
]
