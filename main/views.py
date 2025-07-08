from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Category,DealoftheDay,Customize,BestSeller,Product,Carousel,Configration
from .serializers import *
from customer.serializer import TenentDisplaySerializer
from utils import get_response,CustomPageNumberPagination
from rest_framework import status,permissions,parsers
from django.db.models import Count,Q,Sum
from invoice.models import Invoice,InvoiceItem
from .util import get_today_time_slots,get_tomorrow_time_slots
class CategoryView(APIView):
    def get(self, request):
        data  =request.GET
        try:
            if data.get('id'):
                categories = Category.objects.get(id=data.get('id'))

                serializer = CategorySerializer(categories)
                return get_response(False,serializer.data,status.HTTP_200_OK)
            elif data.get('name'):
                categories = Category.objects.filter(name__iexact=data.get('name'),is_available=True).first()
                serializer = CategorySerializer(categories )
                return get_response(False,serializer.data,status.HTTP_200_OK)
            else:
                if request.user and request.user.is_authenticated and request.user.is_admin:
                    categories = Category.objects.all().order_by('sort_order')
                else:


                    categories = Category.objects.annotate(
                        count=Count('product', filter=Q(product__is_available=True))
                    ).filter(count__gte=1, is_available=True).order_by('sort_order')

                serializer = CategorySerializer(categories, many=True)

                return get_response(False,serializer.data,status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return get_response(True,str(e),status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        if request.user and request.user.is_authenticated and request.user.is_admin:

            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                return get_response(False,serializer.data,status.HTTP_201_CREATED)
            else:
                return get_response(True,serializer.errors,status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Must be an admin user"}, status=status.HTTP_401_UNAUTHORIZED)
    def put(self,request):
        if request.user and request.user.is_authenticated and request.user.is_admin:

            try:
                category = Category.objects.get(id=request.data.get('id'))
                serializer = CategorySerializer(instance=category,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    deals = Category.objects.get(id=serializer.data.get('id'))
                    serializer = CategorySerializer(deals)
                    return get_response(False, serializer.data, status.HTTP_201_CREATED)
                else:
                    return get_response(True, serializer.errors, status.HTTP_400_BAD_REQUEST)
            except Category.DoesNotExist:
                return get_response(True, 'Category  with this id not exits', status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Must be an admin user"}, status=status.HTTP_401_UNAUTHORIZED)
    def delete(self, request):
        if request.user and request.user.is_authenticated and request.user.is_admin:
            data = request.data
            Category_id = data.get('id')
            paginator  = CustomPageNumberPagination()
            if Category_id is None:
                return Response({"error": "ID must be provided"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                category = Category.objects.get(id=Category_id)
                category.is_available = not category.is_available
                category.save()

                if not category.is_available:
                    Product.objects.filter(category=category).update(is_available=False)
                category = Category.objects.all().order_by('sort_order')
                page = paginator.paginate_queryset(category, request)
                if page is not None:
                    serializer = CategorySerializer(page, many=True)
                    return paginator.get_paginated_response(serializer.data)
                serializer = CategorySerializer(category, many=True)
                return get_response(False,serializer.data,status.HTTP_200_OK)
            except Category.DoesNotExist:
                return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Must be an admin user"}, status=status.HTTP_401_UNAUTHORIZED)

class DealView(APIView):
    def get(self, request):
        deal_id = request.query_params.get('id')  # Use query parameters
        try:
            if deal_id:
                deal = DealoftheDay.objects.get(id=deal_id)
                serializer = DealoftheDaySerializer(deal)
                return get_response(False, serializer.data, status.HTTP_200_OK)
            else:
                deals = DealoftheDay.objects.all()
                if not (request.user and request.user.is_authenticated and request.user.is_admin):
                    deals = DealoftheDay.objects.filter(is_available=True)

                serializer = DealoftheDaySerializer(deals, many=True)
                return get_response(False, serializer.data, status.HTTP_200_OK)
        except DealoftheDay.DoesNotExist:
            return get_response(True, "Deal not found.", status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return get_response(True, str(e), status.HTTP_400_BAD_REQUEST)
    def post(self,request):
        if request.user and request.user.is_authenticated and request.user.is_admin:

            serializer = DealoftheDayuploadSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                deals = DealoftheDay.objects.get(id=serializer.data.get('id'))
                serializer = DealoftheDaySerializer(deals)
                return get_response(False, serializer.data, status.HTTP_201_CREATED)
            else:
                return get_response(True, serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Must be an admin user"}, status=status.HTTP_401_UNAUTHORIZED)
    def put(self,request):
        if request.user and request.user.is_authenticated and request.user.is_admin:

            try:
                deal = DealoftheDay.objects.get(id=request.data.get('id'))
                serializer = DealoftheDayuploadSerializer(instance=deal,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    deals = DealoftheDay.objects.get(id=serializer.data.get('id'))
                    serializer = DealoftheDaySerializer(deals)
                    return get_response(False, serializer.data, status.HTTP_201_CREATED)
                else:
                    return get_response(True, serializer.errors, status.HTTP_400_BAD_REQUEST)
            except DealoftheDay.DoesNotExist:
                return get_response(True, 'Deal of the day with this id not exits', status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Must be an admin user"}, status=status.HTTP_401_UNAUTHORIZED)
    def patch(self, request):
        if request.user and request.user.is_authenticated and request.user.is_admin:
            data = request.data

            Deal_id = data.get('data')
            Deal_id = Deal_id.get('id')
            paginator  = CustomPageNumberPagination()
            if Deal_id is None:
                return Response({"error": "ID must be provided"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                Deal = DealoftheDay.objects.get(id=Deal_id)
                Deal.is_available =  not Deal.is_available
                Deal.save()
                Deal = DealoftheDay.objects.all()
                page = paginator.paginate_queryset(Deal, request)
                if page is not None:
                    serializer = DealoftheDaySerializer(page, many=True)
                    return paginator.get_paginated_response(serializer.data)
                serializer = DealoftheDaySerializer(Deal, many=True)
                return get_response(False,serializer.data,status.HTTP_200_OK)
            except DealoftheDay.DoesNotExist:
                return Response({"error": "Deal not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Must be an admin user"}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        if request.user and request.user.is_authenticated and request.user.is_admin:
            data = request.data
            Deal_id = data.get('id')
            paginator  = CustomPageNumberPagination()
            if Deal_id is None:
                return Response({"error": "ID must be provided"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                Deal = DealoftheDay.objects.get(id=Deal_id)
                Deal.delete()
                Deal = DealoftheDay.objects.all()
                page = paginator.paginate_queryset(Deal, request)
                if page is not None:
                    serializer = DealoftheDaySerializer(page, many=True)
                    return paginator.get_paginated_response(serializer.data)
                serializer = DealoftheDaySerializer(Deal, many=True)
                return get_response(False,serializer.data,status.HTTP_200_OK)
            except DealoftheDay.DoesNotExist:
                return Response({"error": "Deal not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Must be an admin user"}, status=status.HTTP_401_UNAUTHORIZED)

class CustomizeView(APIView):
    def get(self, request, product_id):
        customize = Customize.objects.filter(product_id=product_id)
        serializer = CustomizeSerializer(customize, many=True)
        return get_response(False, serializer.data, status.HTTP_200_OK)

class BestSellerView(APIView):
    def get(self, request):
        best_sellers = BestSeller.objects.filter(
            product__is_available=True,
            product__category__is_available=True
        )
        serializer = BestSellerSerializer(best_sellers, many=True)
        return get_response(False, serializer.data, status.HTTP_200_OK)

class Productsview(APIView):
    parser_classes = [parsers.MultiPartParser]

    def get(self, request):
        category = request.GET.get('category', '')
        product_id = request.GET.get('id', '')
        search = request.GET.get('search', '').strip()
        is_piece = request.GET.get('is_piece')
        code = request.GET.get('code','')

        is_paginated = request.GET.get('is_paginated') != 'false'
        paginator = CustomPageNumberPagination()

        # Handle case for specific product ID

        if product_id:
            try:
                product = Product.objects.get(id=int(product_id))
                serializer = ProductMainSerializer(product)
                return get_response(False, serializer.data, status.HTTP_200_OK)
            except Product.DoesNotExist:
                return get_response(True, 'Product not exists', status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return get_response(True, str(e), status.HTTP_400_BAD_REQUEST)
        if code:
            try:
                product = Product.objects.get(code=code)
                serializer = ProductMainSerializer(product)
                return get_response(False, serializer.data, status.HTTP_200_OK)
            except Product.DoesNotExist:
                return get_response(True, 'Product not exists', status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return get_response(True, str(e), status.HTTP_400_BAD_REQUEST)
        # Construct the product query based on search and filters
        product_query = Q()
        if search:
            product_query |= Q(name__icontains=search)
            product_query |= Q(category__name__icontains=search)
            product_query |= Q(price__icontains=search)
            product_query |= Q(code__icontains=search)

        # Handle category filter
        if category:
            product = Product.objects.filter(category__name__iexact=category).order_by('sort_order')
            if is_paginated is False:
                serializer = ProductMainSerializer(product, many=True)
                return get_response(False, serializer.data, status.HTTP_200_OK)
        else:
            product = Product.objects.all().order_by('sort_order')
            if is_paginated is False:
                serializer = ProductMainSerializer(product, many=True)
                return get_response(False, serializer.data, status.HTTP_200_OK)

        # Apply the product_query for search-based filtering
        product = product.filter(product_query)

        # Filter by availability if not an admin
        if not (request.user and request.user.is_authenticated and request.user.is_admin):
            product = product.filter(is_available=True)

        # Filter by `is_piece` if specified
        if is_piece == 'true':
            product = product.filter(is_piece=True)
        elif is_piece == 'false':
            product = product.filter(is_piece=False)

        # Handle empty product set
        if not product.exists():
            return get_response(True, "No Product found", status.HTTP_404_NOT_FOUND)

        # Pagination

        page = paginator.paginate_queryset(product, request)
        if page is not None:
            serializer = ProductMainSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # Non-paginated response
        serializer = ProductMainSerializer(product, many=True)
        return get_response(False, serializer.data, status.HTTP_200_OK)

    def post(self,request):

        if request.user and request.user.is_authenticated and request.user.is_admin:
            data = request.data
            serializer = ProductUploadSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                product = Product.objects.get(id=serializer.data.get('id'))
                data = ProductMainSerializer(product).data
                return get_response(False,data,status.HTTP_201_CREATED)
            else:
                return get_response(True,serializer.errors,status.HTTP_400_BAD_REQUEST)

        else:
            return get_response(True,'Must be a admin user',status.HTTP_401_UNAUTHORIZED)
    def put(self,request):
        if request.user and request.user.is_authenticated and request.user.is_admin:

            try:
                product = Product.objects.get(id=request.data.get('id'))
                serializer = ProductUploadSerializer(instance=product,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    products = Product.objects.get(id=serializer.data.get('id'))
                    serializer = ProductMainSerializer(products)
                    return get_response(False, serializer.data, status.HTTP_201_CREATED)
                else:
                    return get_response(True, serializer.errors, status.HTTP_400_BAD_REQUEST)
            except Product.DoesNotExist:
                return get_response(True, 'Product  with this id not exits', status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Must be an admin user"}, status=status.HTTP_401_UNAUTHORIZED)
    def delete(self, request):
        if request.user and request.user.is_authenticated and request.user.is_admin:
            data = request.data
            product_id = data.get('id')
            paginator  = CustomPageNumberPagination()
            if product_id is None:
                return Response({"error": "ID must be provided"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                product = Product.objects.get(id=product_id)
                if product.is_available == False and product.category.is_available ==False:
                    return Response({"error": "The category is not available"}, status=status.HTTP_400_BAD_REQUEST)
                product.is_available = not product.is_available
                product.save()
                product = Product.objects.all().order_by('sort_order')
                page = paginator.paginate_queryset(product, request)
                if page is not None:
                    serializer = ProductMainSerializer(page, many=True)
                    return paginator.get_paginated_response(serializer.data)
                serializer = ProductMainSerializer(product, many=True)
                return get_response(False,serializer.data,status.HTTP_200_OK)
            except Product.DoesNotExist:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Must be an admin user"}, status=status.HTTP_401_UNAUTHORIZED)
class CategorypagignatedView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        data  =request.GET
        try:
            paginator = CustomPageNumberPagination()

            if data.get('search'):
                category_query = Q(name__icontains=data.get('search'))
                category = Category.objects.filter(category_query).order_by('sort_order')
                page = paginator.paginate_queryset(category, request)
                if page is not None:
                    serializer = CategorySerializer(page, many=True)
                    return paginator.get_paginated_response(serializer.data)
                serializer = CategorySerializer(category, many=True)
                return get_response(False,serializer.data,status.HTTP_200_OK)
            else:
                category = Category.objects.all().order_by('sort_order')
                page = paginator.paginate_queryset(category, request)
                if page is not None:
                    serializer = CategorySerializer(page, many=True)
                    return paginator.get_paginated_response(serializer.data)
                serializer = CategorySerializer(category, many=True)
                return get_response(False,serializer.data,status.HTTP_200_OK)
        except Exception as e:
            return get_response(True,str(e),status.HTTP_400_BAD_REQUEST)

class DealpagignatedView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        data = request.GET
        try:
            paginator = CustomPageNumberPagination()

            if data.get('id'):
                deal = DealoftheDay.objects.get(id=data.get('id'))
                serializer = DealoftheDaySerializer(deal)
                return get_response(False, serializer.data, status.HTTP_200_OK)

            elif data.get('search'):
                category_query = Q(Q(product__name__icontains=data.get('search'))|Q(price__icontains=data.get('search')))
                category = DealoftheDay.objects.filter(category_query)
                page = paginator.paginate_queryset(category, request)
                if page is not None:
                    serializer = DealoftheDaySerializer(page, many=True)
                    return paginator.get_paginated_response(serializer.data)
                serializer = DealoftheDaySerializer(category, many=True)
                return get_response(False,serializer.data,status.HTTP_200_OK)
            else:
                deals = DealoftheDay.objects.all()
                page = paginator.paginate_queryset(deals, request)
                serializer = DealoftheDaySerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return get_response(True, str(e), status.HTTP_400_BAD_REQUEST)

class CustomizepagignatedView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        data = request.GET
        try:
            paginator = CustomPageNumberPagination()
            if data.get('search'):
                category_query = Q(Q(product__name__icontains=data.get('search'))|Q(name__icontains=data.get('search')))
                category = Customize.objects.filter(category_query)
                page = paginator.paginate_queryset(category, request)
                if page is not None:
                    serializer = CustomizeSerializer(page, many=True)
                    return paginator.get_paginated_response(serializer.data)
                serializer = CustomizeSerializer(category, many=True)
                return get_response(False,serializer.data,status.HTTP_200_OK)
            else:
                customize = Customize.objects.all()
                page = paginator.paginate_queryset(customize, request)
                serializer = CustomizeSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return get_response(True, str(e), status.HTTP_400_BAD_REQUEST)

class BestSellerpagignatedView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        data = request.GET
        try:
            paginator = CustomPageNumberPagination()
            if data.get('search'):
                category_query = Q(product__name__icontains=data.get('search'))
                category = BestSeller.objects.filter(category_query)
                page = paginator.paginate_queryset(category, request)
                if page is not None:
                    serializer = BestSellerSerializer(page, many=True)
                    return paginator.get_paginated_response(serializer.data)
                serializer = BestSellerSerializer(category, many=True)
                return get_response(False,serializer.data,status.HTTP_200_OK)
            else:
                best_sellers = BestSeller.objects.all()
                page = paginator.paginate_queryset(best_sellers, request)
                serializer = BestSellerSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return get_response(True, str(e), status.HTTP_400_BAD_REQUEST)



class Timeslotview(APIView):
    def get(self,request):
        timeslottoday,datetoday =  get_today_time_slots()
        timeslottomorrow,datetomorrow =  get_tomorrow_time_slots()
        return Response({'today':{'timeslote':timeslottoday,'date':datetoday},'tomorrow':{'timeslote':timeslottomorrow,'date':datetomorrow}})


class Producteditview(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, id):
        if request.user and request.user.is_authenticated and request.user.is_admin:

            if id:
                try:
                    product = Product.objects.get(id=int(id))
                    serializer = ProducteditgetSerializer(product).data
                    return get_response(False, serializer, status.HTTP_200_OK)
                except Product.DoesNotExist:
                    return get_response(True, 'Product does not exist', status.HTTP_404_NOT_FOUND)
                except Exception as e:
                    return get_response(True, str(e), status.HTTP_400_BAD_REQUEST)
            else:
                return get_response(True, 'Product ID is required', status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Must be an admin user"}, status=status.HTTP_401_UNAUTHORIZED)


class ProductCustomize(ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = ProductInvoicegetSerializer
    pagination_class = None


class Saledetailview(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        start_date = request.GET.get("startDate")
        end_date = request.GET.get("endDate")




        invoice_filter = {}
        if start_date:
            invoice_filter["created_at__gte"] = start_date
        if end_date:
            invoice_filter["created_at__lte"] = end_date

        invoices = Invoice.objects.filter(**invoice_filter)

        total = invoices.aggregate(total_sales=Sum("items__sub_total"))["total_sales"]
        count = invoices.annotate(count=Count('items')).filter(count__gte=1).count()

        product_sales = (
            InvoiceItem.objects
            .filter(invoice__in=invoices)
            .values('productcustomize__name')
            .annotate(total_sales=Sum('sub_total'),total_count=Sum('count'))
            .order_by('-total_sales')
        )

        return get_response(False, {
            'count': count,
            'total': total,
            'product_sales': product_sales
        }, status=status.HTTP_200_OK)




class Carouselview(APIView):
    def get(self, request):
        carousel = Carousel.objects.all()
        serializer = CarouselSerializer(carousel, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user and request.user.is_authenticated and request.user.is_admin:
            serializer = CarouselSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Must be an admin user"}, status=status.HTTP_401_UNAUTHORIZED)
    def delete(self, request ):
        if request.user and request.user.is_authenticated and request.user.is_admin:
            pk = request.data.get('id')
            if pk is None:
                return Response(
                    {"detail": "Provide an ID to delete an object."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                carousel = Carousel.objects.get(pk=pk)
                carousel.delete()
                serializer = CarouselSerializer(Carousel.objects.all(),many=True)
                return get_response(False,serializer.data,status.HTTP_200_OK)
            except Carousel.DoesNotExist:
                return Response({"detail": "Object not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Must be an admin user"}, status=status.HTTP_401_UNAUTHORIZED)
        
class TenentsUser(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request): 
        serializer = TenentDisplaySerializer(request.tenant )
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class Configrationview(APIView):
    def post(self,request):
        data = request.data
        serializer = ConfigSettingsSerializer(data=data)
        if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED) 
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request):
        serializer = ConfigSettingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(None, serializer.validated_data)
            return Response({"detail": "Configuration updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self,request):
        param_name = request.GET.get('param_name')
        if  param_name:
            c = Configration.objects.filter(parameter_name__icontains = param_name).first()
            data = ConfigrationSerializer(data)
            return Response(data.data, status=status.HTTP_200_OK) 

        c = Configration.objects.all()
        serail = ConfigrationSerializer(c,many=True)
        return Response(serail.data, status=status.HTTP_200_OK) 

 
