from django.urls import path
from .views import *
from invoice.views import Invoiceview 
urlpatterns = [
    path('category/',CategoryView.as_view(),name='category'), 
    path('deal/',DealView.as_view(),name='deal'), 
    path('customize/<int:product_id>/',CustomizeView.as_view(),name='customize'), 
    path('best-seller/',BestSellerView.as_view(),name='best-seller'), 
    path('products/',Productsview.as_view(),name='product'),
    path('category-pagignated/',CategorypagignatedView.as_view(),name='timeslot'),
    path('bestseller-pagignated/',BestSellerpagignatedView.as_view(),name='timeslot'),
    path('dealofday-pagignated/',DealpagignatedView.as_view(),name='timeslot'),
    path('customize-pagignated/',CustomizepagignatedView.as_view(),name='timeslot'),
    path('get-timeslot/',Timeslotview.as_view(),name='timeslot'),
    path('products-edit/<int:id>/',Producteditview.as_view(),name='product'),

    path('invoice/',Invoiceview.as_view()),
    path('product-customize/',ProductCustomize.as_view()),
    path('sale-details/',Saledetailview.as_view()),
    path('carousel/',Carouselview.as_view()),
    path('user-tenent-fetch/',TenentsUser.as_view()),
    path('carousel/',Carouselview.as_view()),
    path('configration/',Configrationview.as_view()),








]