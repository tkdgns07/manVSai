from django.contrib import admin
from django.urls import path
from core.chartDataAPI import extract_csv_data
from core.optionPricingAPI import optionPricing

urlpatterns = [
    path("admin/", admin.site.urls),
    path("extract_csv_data/", extract_csv_data),
    path("option_pricing/", optionPricing)
]