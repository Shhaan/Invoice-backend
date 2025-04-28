from django.urls import path
from .views import * 

urlpatterns = [
 
    path('generate-pdf/<int:id>/', generatepdf),
    path('generate-kichen-pdf/<int:id>/', generatekichenpdf),


 

 
] 
