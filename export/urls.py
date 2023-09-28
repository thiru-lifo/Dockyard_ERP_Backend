from django.urls import path
from . import views

urlpatterns = [
   # path('gettoken/', TokenObtainPairView.as_view(), name = 'gettoken'),
    #path('refreshtoken/', TokenRefreshView.as_view(), name = 'refreshtoken'),
    #path('verifytoken/', TokenVerifyView.as_view(), name = 'verifytoken'),

    path('ipl',views.IPLViews.as_view(), name = 'ipl'),
    path('pdfgen/',views.GeneratePDFViews.as_view(), name= 'pdfgen'),
    


]