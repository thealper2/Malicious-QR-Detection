from django.urls import path
from server.views import classify_qr_code

urlpatterns = [
    path("", classify_qr_code, name="classify_qr_code"),
]
