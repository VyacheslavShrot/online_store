from django.urls import path

from core.views import IndexView, SupportView, ReportView

app_name = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("support/", SupportView.as_view(), name="support"),
    path("report/", ReportView.as_view(), name="report"),
]
