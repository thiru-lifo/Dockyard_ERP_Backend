
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
#from rest_framework import authentication, AllowAny
#from rest_framework.permissions import Is_Authenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

import xlwt
from django.http import HttpResponse
from .utils import render_to_pdf
from .models import IPL
from .serializer import IPLserializer
from django.template.loader import get_template
#import pdfkit
from django.http import HttpResponse
#from serializers import serialize
import datetime


# Create your views here.

class GeneratePDFViews(APIView):

    def get(self, request, *args, **kwargs):
        template = get_template('export/test.html')
        context = {
             'today': datetime.date.today(), 
             'amount': 799,
            'customer_name': 'ETMA',
            #'order_id': 1233434,
        }
        html = template.render(context)
        pdf = render_to_pdf('export/test.html', context)
        if pdf:
            response = HttpResponse(pdf,content_type='application/pdf')
            filename = "Pdf_%s.pdf" %("123")
            content = "inline; filename='%s'"%(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'"%(filename)
            response['Content-Disposition'] = content 
            return response
        return HttpResponse("Not found")






class IPLViews(APIView):
#Export excel
    def post(self,request):

        saveserialize = IPLserializer(data = request.data)
        if saveserialize.is_valid():

            saveserialize.save()

            # content-type of response
            response = HttpResponse(content_type='application/ms-excel')

            #decide file name
            response['Content-Disposition'] = 'attachment; filename="IPL.xls"'

            #creating workbook
            wb = xlwt.Workbook(encoding='utf-8')

            #adding sheet
            ws = wb.add_sheet("IPL")

            # Sheet header, first row
            row_num = 0

            font_style = xlwt.XFStyle()
            # headers are bold
            font_style.font.bold = True

            #column header names, you can use your own headers here
            columns = ['team', 'captain', 'city']

            #write column headers in sheet
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, str(columns[col_num]), font_style)

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()

            #get your context, from contextbase or from a text file...

            data = IPL.objects.all()
            #context = get_context() #dummy method to fetch context.

            for my_row in data:
                row_num = row_num + 1
                ws.write(row_num, 0, my_row.team, font_style)
                ws.write(row_num, 1, my_row.captain, font_style)
                ws.write(row_num, 2, my_row.city, font_style)
            
            wb.save(response)
            return response

            #return Response({"status" : "context Inserted Successfully", "context":saveserialize.context}, status=status.HTTP_200_OK)
        else:
            return Response({"status" : "context Insert Failed", "context":saveserialize.errors}, status=status.HTTP_400_BAD_REQUEST)






        
        

        

        

        

      