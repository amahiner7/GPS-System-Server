from django.urls import path
from . import views
from .display_gps_score_view import DisplayGPSScoreView

# app_name = "display_gps_score_app"

urlpatterns = [
    # path("", DisplayGPSScoreView.as_view(), name="index"),
    # path("/<str:param>", views.index, name="index"),
    path("/<str:param>", DisplayGPSScoreView.as_view(), name="display_gps_score"),
    # path("request/<str:param>", views.index, name="index"),
    # path("request/", views.index, name="index"),
    # path("request/<str:param>/", DisplayGPSScoreView.as_view(), name="display_gps_score"),
]
