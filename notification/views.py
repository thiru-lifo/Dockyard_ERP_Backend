from functools import reduce
import operator
from pickle import FALSE
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Notification,Smtpconfigure
from .serializer import Notificationserializer,Smtpconfigureserializer
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings                                                                                                                                                       
from django.http import HttpResponse
from twilio.rest import Client
from NavyTrials import language
from .models import Notification,Smtpconfigure,NotificationUser,NotificationUserLog
from .serializer import NotificationUserSerializer
from django.db.models import Q,DurationField, F, ExpressionWrapper ,DateTimeField,DateField
from NavyTrials import language,error,settings,common
from master import models as masterModels
from transaction import models as transactionModels
from master import serializer as masterSerializer
from access import models as accessModels
from access import models as accessSerializer
from . import models

  
class SmtpconfigureViews(APIView):

    def post(self, request, format=None):
        
        serializer = Smtpconfigureserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Success", "data": serializer.data}, status=status.HTTP_200_OK)
       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificationViews(generics.GenericAPIView):

    serializer_class = Notificationserializer

    def post(self,request):
        notification = request.data    
        serializer = Notificationserializer(data = notification)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        notification = serializer.data
        if notification['type'] == 2:
            #notification = Notification.objects.get(to=notification_data['to'])
            # token = RefreshToken.for_user(notification).access_token
            # current_site = get_current_site(request).domain
            # relativeLink = reverse('email-verify')
            # absurl = 'http://'+current_site+relativeLink+"?token"+str(token)
            
            # email_body= 'Hi '+notification['message']+'\n Use below link to verfy your email \n'
            email_body= 'Hi '+notification['message']
            data = {'email_body' : email_body, 'to_email' : notification['to'], 'email_subject':'verify your email'}
            Util.send_email(data)
            return Response({"status" :"success","message":+language.context[language.defaultLang]['email send'], "data" : 'test'}, status=status.HTTP_200_OK)

        else:
           
            message_to_broadcast = ("pink ")
                                                        
            print('hi')                                            
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            for recipient in settings.SMS_BROADCAST_TO_NUMBERS:
                if recipient:
                    client.messages.create(to=recipient,
                                        from_=settings.TWILIO_NUMBER,
                                        body=message_to_broadcast)
            # return HttpResponse("messages sent!", 200)

            return Response({"status" : "success","message":+language.context[language.defaultLang]['sms sent'], "data" : 'test'}, status=status.HTTP_200_OK)

            
class VerifyEmail(generics.GenericAPIView):
    def get(self):
        pass



class getNotifications(APIView):
    # authentication_classes = [] #disables authentication
    # permission_classes = [] #disables permission
    def post(self,request, pk = None):


        h_type = request.data['h_type']
        user_id = request.data['user_id']

        if h_type!="":
            notificationsDet=models.NotificationUser.objects.values('id','message','created_on','transaction_id','form_id','project_id','from_user_id','to_user_id').filter(user_role_id__isnull = False, hierarchy_type = h_type, to_user_id = user_id)
            #print(notificationsDet.query,"notificationsDet1", h_type)
        else:
            notificationsDet=models.NotificationUser.objects.values('id','message','created_on','transaction_id','form_id','project_id','from_user_id','to_user_id').filter(user_role_id__isnull = False)
            #print(notificationsDet.query,"notificationsDet2", h_type)

        if 'Authorized-Role' in request.headers:
            role_code=request.headers['Authorized-Role']
            user_role_id=request.headers['Authorized-By']
            process_id=request.user.process_id if request.user.process_id else None
            notificationsDet=notificationsDet.exclude(id__in=models.NotificationUserLog.objects.values('notification_id').filter(user_id=request.user.id,user_role_id=user_role_id))
            
            if role_code!='admin':

                # Commented --------------------------------------------------------
                #notificationsDet=notificationsDet.filter(Q(user_role_id=user_role_id) & Q(process_id=process_id))
                # Commented --------------------------------------------------------

                #form_ids=transactionModels.DataAccessForms.objects.values('form_id').filter(user_id=request.user.id)
                # modules=masterModels.DataAccess.objects.values('module_id').filter(user_id=request.user.id)
                # modules=transactionModels.FormsMapping.objects.values('module_id').filter(form_id__in=(transactionModels.DataAccessForms.objects.values('id').filter(user_id=request.user.id))).distinct('module_id')
                # sub_modules=masterModels.DataAccessSubModule.objects.values('sub_module_id').filter(data_access__user_id=request.user.id)
                # sub_modules=transactionModels.FormsMapping.objects.values('sub_module_id').filter(form_id__in=(transactionModels.DataAccessForms.objects.values('id').filter(user_id=request.user.id))).distinct('sub_module_id')
                # notificationsDet=notificationsDet.filter(module_id__in=modules,sub_module_id__in=sub_modules)

                # Commented ------------------------------------------
                #notificationsDet=notificationsDet.filter(form_id__in=form_ids)
                # Commented ------------------------------------------
                pass

        #print(notificationsDet.order_by('-id').query,"@@@@@@@@@@")

        notificationsDet=notificationsDet.order_by('-id')

        return Response({"status":error.context['success_code'], "data": notificationsDet}, status=status.HTTP_200_OK)


class saveNotificationLog(APIView):
    
    def post(self,request, pk = None):
        if 'notification_id' not in request.data:
            return Response({"status":error.context['error_code'],"message" : "notification_id" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else:
            user_role_id=request.headers['Authorized-By'] if 'Authorized-By' in request.headers else None
            NotificationUserLog.objects.create(notification_id=request.data['notification_id'],user_id=request.user.id,user_role_id=user_role_id)
            return Response({"status":error.context['success_code'], "message": 'Log saved successfully'}, status=status.HTTP_200_OK)