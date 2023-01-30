from django.urls import path
from . import views
from .display_gps_score_view import DisplayGPSScoreView

# app_name = "display_gps_score_app"

urlpatterns = [
    path("/<str:param>", DisplayGPSScoreView.as_view(), name="display_gps_score"),
]
