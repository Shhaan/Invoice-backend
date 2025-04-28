from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from utils import get_response, CustomPageNumberPagination
from .serializer import Invoiceserializer,Invoicepdfserializer
from django.db.models import Q,Count
from .models import Invoice,InvoiceItem
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from urllib.parse import unquote
from django.templatetags.static import static


class Invoiceview(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = request.GET
        search = data.get('search')
        invoice = Invoice.objects.annotate(count=Count('items')).filter(count__gte=1).order_by('-id')
        paginator = CustomPageNumberPagination()
        page = paginator.paginate_queryset(invoice, request)
          
        try:
            if data.get('id'):
                
                
                invoice = Invoice.objects.annotate(count=Count('items')).filter(count__gte=1,id=data.get('id')).first()
                if not invoice:
                    return get_response(True, "Invoice dosn't exists", status.HTTP_400_BAD_REQUEST)
                serializer = Invoiceserializer(invoice)
                return get_response(False, serializer.data, status.HTTP_200_OK)
            
            elif search:
                invoice_query =   Q(id__startswith=search)   
                invoice = Invoice.objects.annotate(count=Count('items')).filter(Q(count__gte=1)&Q(invoice_query)).order_by('-id')
                page = paginator.paginate_queryset(invoice, request)
                
                if page is not None:
                    serializer = Invoiceserializer(page, many=True)
                    return paginator.get_paginated_response(serializer.data)
                
                serializer = Invoiceserializer(invoice, many=True)
                return get_response(False, serializer.data, status.HTTP_200_OK)
            
            else:
                if page is not None:
                    serializer = Invoiceserializer(page, many=True)
                    return paginator.get_paginated_response(serializer.data)
                
                serializer = Invoiceserializer(invoice, many=True)
                return get_response(False, serializer.data, status.HTTP_200_OK)
        
        except Exception as e:
            return get_response(True, str(e), status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = Invoiceserializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return get_response(False, serializer.data, status.HTTP_201_CREATED)
        
        return get_response(True, serializer.errors, status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            invoice_id = request.data.get('invoiceid')
        
            if not invoice_id:
                return get_response(True, "Invoice ID is required", status.HTTP_400_BAD_REQUEST)
            
            invoice = Invoice.objects.get(id=invoice_id)
            InvoiceItem.objects.filter(invoice=invoice).delete()
            
            serializer = Invoiceserializer(invoice, data=request.data )
            
            if serializer.is_valid():
                serializer.save()
                return get_response(False, serializer.data, status.HTTP_200_OK)
            
            return get_response(True, serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        except Invoice.DoesNotExist:
            return get_response(True, "Invoice not found", status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return get_response(True, str(e), status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        paginator  = CustomPageNumberPagination()

        try:
            invoice_id = request.data.get('id')
            if not invoice_id:
                return get_response(True, "Invoice ID is required", status.HTTP_400_BAD_REQUEST)
            
            invoice = Invoice.objects.get(id=invoice_id)
            invoice.delete()
            invoice = Invoice.objects.all().order_by('-id')
            page = paginator.paginate_queryset(invoice, request)
            if page is not None:
                serializer = Invoiceserializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            serializer = Invoiceserializer(invoice, many=True)
            return get_response(False,serializer.data,status.HTTP_200_OK)
        
        except Invoice.DoesNotExist:
            return get_response(True, "Invoice not found", status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return get_response(True, str(e), status.HTTP_400_BAD_REQUEST)

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if pdf.err:
        return HttpResponse("Invalid PDF", status=400, content_type='text/plain')
    return HttpResponse(result.getvalue(), content_type='application/pdf')

@api_view(['GET'])
@permission_classes([IsAdminUser])
def generatepdf(request, id):
    try:
        invoice = Invoice.objects.get(id=id)
    except Invoice.DoesNotExist:
        return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)
    data = Invoicepdfserializer(invoice).data

    logo_url = request.build_absolute_uri(static('invoice/bg.png'))
    qr = request.build_absolute_uri(static('invoice/qr.jpg'))  
    context = {
        'id': data['id'],
        'name': data['name'],
         
        'time_slot': data['time_slot'],
        'items': data['items'],
        'total': data['total'],
        'is_delivery': data['is_delivery'],
        'building': data['building'],
        'Street': data['Street'],
        'Zone': data['Zone'],
        'logo_url': unquote(logo_url),  
        'qr' :unquote(qr),
        'location': data['location'],

    }

    response = render_to_pdf("invoice/Pdftemplate.html", context)
    
    if response.status_code == 400:
        return Response({"error": "Error generating PDF"}, status=status.HTTP_400_BAD_REQUEST)

    filename = "Statement_form.pdf"
    content = f"attachment; filename={filename}"
    response["Content-Disposition"] = content

    return response





@api_view(['GET'])
@permission_classes([IsAdminUser])
def generatekichenpdf(request, id):
    try:
        invoice = Invoice.objects.get(id=id)
    except Invoice.DoesNotExist:
        return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)
    data = Invoicepdfserializer(invoice).data

    logo_url = request.build_absolute_uri(static('invoice/bg.png'))
    qr = request.build_absolute_uri(static('invoice/qr.jpg'))
 

    context = {
        'id': data['id'],
        'name': data['name'],
         
        'location': data['location'],

        'time_slot': data['time_slot'],
        'items': data['items'],
        'total': data['total'],
        'is_delivery': data['is_delivery'],
        'building': data['building'],
        'Street': data['Street'],
        'Zone': data['Zone'],
  
    }

    response = render_to_pdf("invoice/Pdfkichen.html", context)
    
    if response.status_code == 400:
        return Response({"error": "Error generating PDF"}, status=status.HTTP_400_BAD_REQUEST)

    filename = "Statement_form.pdf"
    content = f"attachment; filename={filename}"
    response["Content-Disposition"] = content

    return response