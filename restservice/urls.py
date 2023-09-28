from django.urls import path
from . import views

urlpatterns = [
    path('visa-validation',views.VisaValidation.as_view(), name = 'visaValidation'),
    path('visa-validation-testing',views.VisaValidationTesting.as_view(), name = 'VisaValidationTesting'),
]    