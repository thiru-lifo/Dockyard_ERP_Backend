from telnetlib import STATUS
from django.shortcuts import render
from access import models

# Create your views here.
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenViewBase

from .serializer import MyTokenObtainSerializer, MyTokenRefreshSerializer, UserListSerializer, UserListHierarchySerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializer import Userserializer
from master.serializer import DesignationSerializer
from rest_framework import status
from access.views import Common
from log.models import UserLogin
from datetime import datetime
from NavyTrials import language,error
from notification.utils import Util
from django.template import loader
from configuration.models import Templatestable
from django.template import Context, Template
from configuration.models import Configurationtable,RoleConfiguration,Templatestable
from configuration.serializer import Configurationtableserializer
from django.utils.crypto import get_random_string
from access.models import RolesPermissions,AccessUserRoles,UserRoleMapping
from master.models import Designation, DataAccess, DataAccessSubModule
from master.serializer import DataAccessSerializerCRUD
from . import models
from . import serializer


from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import csv
from transaction import models as transactionModels

# Added - Starts
from functools import reduce
import operator
from django.db.models import Q
# Added - End

class MyTokenObtainPairView(TokenViewBase):
    #def post(self, request, *args, **kwargs):
    print()
    default_error_messages = {
        'no_active_account': 'Username or Password does not matched.'
    }    
    serializer_class = MyTokenObtainSerializer
                
class MyTokenRefreshView(TokenViewBase):
   
    serializer_class = MyTokenRefreshSerializer

    def post(self, request, *args, **kwargs):

        token = RefreshToken

        if token:
            return Response({'status': error.context['success_code'], "message" :language.context[language.defaultLang]['missing'], 'token': token})
        else:
            return Response({'status' : error.context['error_code'], "message" : language.context[language.defaultLang]['Incorrect username or password']})


class CorrectVerificationCode(APIView):

    def post(self, request):
        data = request.data
        if 'email' not in data:
            return Response({"status":error.context['error_code'],"message" : "Email"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif 'verification_code' not in data:
            return Response({"status":error.context['error_code'],"message" : "Verification code"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else:
            userAvailable=User.objects.filter(email=data['email'],verification_code=data['verification_code'])
            if userAvailable:
                return Response({"status" : error.context['success_code'], "message":language.context[language.defaultLang]['matched']}, status=status.HTTP_200_OK)
            else:
                return Response({"status":error.context['error_code'],"message" : language.context[language.defaultLang]['incorrect code']},status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request):
        data = request.data
        if 'user_id' not in data:
            return Response({"status":error.context['error_code'],"message" : "User id"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else:
            log_browser=request.user_agent.browser.family
            log_version=request.user_agent.browser.version_string
            log_os=request.user_agent.os.family
            log_platform=request.user_agent.device.family
            log_ip=Common.get_client_ip(request)
            log_datetime = datetime.now()
            userlog=UserLogin.objects.create(user_id=data['user_id'],logon_type='logout',log_datetime=log_datetime,log_ip=log_ip,log_browser=log_browser,log_version=log_version,log_os=log_os,log_platform=log_platform).save()
            return Response({"status":error.context['success_code'],"message" :language.context[language.defaultLang]['logout']},status=status.HTTP_200_OK)

class ResendCodeView(APIView):
    def post(self, request):
        data = request.data
        if 'user_id' not in data:
            return Response({"status":error.context['error_code'],"message" : "User id"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else:
            user=(User.objects.values('id','verification_code','email','loginname').filter(id=data['user_id']).first()) 
            print(user)          
            email_data = {'verification_code' : user['verification_code'],'user_name':user['loginname']}
            template=(Templatestable.objects.values('id','title','actual_template','modified_template').filter(code='VFC').first())                       
            if template:
                if template['modified_template']:     
                    template =   template['modified_template']      
                else:   
                    template =  template['actual_template'] 
                t = Template(template)
                c = Context(email_data)
                html= t.render(c)
                
            else:
                html = loader.render_to_string("email/verification-code.html", context=email_data)
        
            Util.send_email({"email_subject":'Your STEMZ Global account verification code',"email_body":html,"to_email":user['email']})
            return Response({"status":error.context['success_code'], "message" : language.context[language.defaultLang]['verification code'] },status=status.HTTP_200_OK)

class authenticationView(APIView):
    def post(self, request):
        if 'user_role_id' not in request.data:
            return Response({"status":error.context['error_code'],"message" : "User role id"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif 'user_id' not in request.data:
            return Response({"status":error.context['error_code'],"message" : "User id"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else:
            center_id= request.data['center_id'] if 'center_id' in request.data and request.data['center_id'] else 0
            user_role_id= request.data['user_role_id'] if 'user_role_id' in request.data else 0
            user_id= request.data['user_id'] if 'user_id' in request.data else 0
            

            user_role_id=request.data['user_role_id']
            user_id=request.data['user_id']
            data = {}
            #biometric =True                                  
            biometricVal=(Configurationtable.objects.values('id','value').filter(code='BM').first()) 
            if biometricVal and biometricVal['value'] and biometricVal['value'].lower() == "true": 
                rolePerm=(RoleConfiguration.objects.values('id','role_id','config_id').filter(role_id=user_role_id,config_id=biometricVal['id']).first())
                if rolePerm: 
                    data['biometric']=True
                    biometric=True
                else:
                    data['biometric']=False
                    biometric=False
            else:
                data['biometric']=False
                biometric=False
            #print(bool(biometricVal['value']))
            if biometric:
                userfp = UserFingerIndex.objects.values("fingerindex__id","fingerindex__name", "fpdata", "user__id").filter(user=user_id)
                        
                data['fpdata'] = userfp

            #twofactverify = True
            twofactor=(Configurationtable.objects.values('id','value').filter(code='2FA').first()) 
            if twofactor and twofactor['value'] and twofactor['value'].lower()=='true':  
                rolePerm=(RoleConfiguration.objects.values('id','role_id','config_id').filter(role_id=user_role_id,config_id=twofactor['id']).first())
                if rolePerm:
                    data['twofactor']=True
                    twofactverify=True
                else:
                    data['twofactor']=False
                    twofactverify=False
            else:
                data['twofactor']=False
                twofactverify=False
            
            if twofactverify:                     
                template=(Templatestable.objects.values('id','title','actual_template','modified_template').filter(code='VFC').first())                       
                vc=get_random_string(length=6, allowed_chars='1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                user=(User.objects.values('id','verification_code','email','loginname').filter(id=user_id).first())          
                email_data = {'verification_code' : vc,'user_name':user['loginname']}
                User.objects.filter(id=user_id).update(verification_code=vc) 
                if template:
                    if template['modified_template']:     
                        template =   template['modified_template']      
                    else:   
                        template =  template['actual_template']     
                    t = Template(template)
                    c = Context(email_data)
                    html=  t.render(c)  
                else:
                    html = loader.render_to_string("email/verification-code.html", context=email_data)
                
                Util.send_email({"email_subject":'Your STEMZ Global account verification code',"email_body":html,"to_email":user['email']})
            return Response({"status":error.context['success_code'],"authentication" : data },status=status.HTTP_200_OK)

class ChangePasswordAPI(APIView):
       
       def post(self, request):
        if 'old_password' not in request.data:
            return Response({"status":error.context['error_code'],"message" : "Old password"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif 'new_password' not in request.data:
            return Response({"status":error.context['error_code'],"message" : "New password"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif 'new_password2' not in request.data:
            return Response({"status":error.context['error_code'],"message" : "Confirm password"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif request.data['new_password'] != request.data['new_password2']:           
            return Response({"status":error.context['error_code'],"message" : "Password and confirm password not match"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else:            
            user_id=request.user.id
            old_password=request.data['old_password']
            new_password=request.data['new_password']            
            user=(User.objects.filter(id=user_id).first())
            if not user.check_password(old_password):
                return Response({"status":error.context['error_code'],"message" :"Wrong old password."}, status=status.HTTP_200_OK)

            # set_password also hashes the password that the user will get
            user.set_password(new_password)
            user.save()

            response = {
                    'status': error.context['success_code'],
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }
            return Response(response)

class userList(APIView):
    def get(self, request, pk = None):       
        filter_values = dict(request.GET.items())
        search_string=order_type=order_column=limit_start=limit_end=''
        normal_values=dict()
        array_values=dict()
        if filter_values:
            for key,values in filter_values.items():
                if values.find("[") !=-1 and values.find("]") !=-1:
                    res = values.strip('][').split(',')
                    array_values[key]=(res)
                else:
                    normal_values[key]=(values)

            strings = ['first_name','last_name']
            search_string = dict((k, normal_values[k]) for k in strings
                                            if k in normal_values)  
            order_column =  request.GET.get('order_column')
            order_type = request.GET.get('order_type')  
            limit_start = request.GET.get('limit_start')
            limit_end = request.GET.get('limit_end')  


            if order_column is not None:                                      
                normal_values.pop('order_column')
            if order_type is not None: 
                normal_values.pop('order_type')  
            if limit_start is not None: 
                normal_values.pop('limit_start')
            if limit_end is not None: 
                normal_values.pop('limit_end')     

            for key in strings:
                if key in normal_values:
                    normal_values.pop(key)

            if search_string:       
                filter_string = None
                for field in search_string:
                    q = Q(**{"%s__contains" % field: search_string[field] })
                    if filter_string:
                        filter_string = filter_string & q
                    else:
                        filter_string = q
        try:
            if pk:
                list = User.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = UserListSerializer(list)
                return Response({"status":error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except User.DoesNotExist:
            return Response({"status" :error.context['error_code'], "message":"User" +language.context[language.defaultLang]['dataNotFound']}, status = status.HTTP_200_OK)

        lists = User.objects.exclude(status=3)
        if normal_values:
            lists = lists.filter(reduce(operator.and_, 
                               (Q(**d) for d in [dict([i]) for i in normal_values.items()])))
        if array_values:
            for key,values in array_values.items():
                queries= [Q(**{"%s__contains" % key: value }) for value in values]
                query=queries.pop()
                for item in queries:
                    query |= item
                lists = lists.filter(query)

        if search_string:
            lists = lists.filter(filter_string)

        if order_type is None: 
            if order_column:
                lists = lists.order_by(order_column)  

        elif order_type in 'asc':
            if order_column:
                lists = lists.order_by(order_column)
            else: 
                lists = lists.order_by('id')   

        elif order_type in 'desc':
            if order_column:
                order_column = '-' + str(order_column)
                lists = lists.order_by(order_column)
            else: 
                lists = lists.order_by('-id') 

        if limit_start and limit_end:
                lists = lists[int(limit_start):int(limit_end)]

        elif limit_start:
                lists = lists[int(limit_start):]

        elif limit_end:
                lists = lists[0:int(limit_end)]           
        
        serializer = UserListSerializer(lists, many=True)
        return Response({"status":error.context['success_code'], "data": serializer.data}, status=status.HTTP_200_OK)

class usersCRUD(APIView):
    def post(self, request):
        if ('status' not in request.data):
            return Response({"status":error.context['error_code'],"message" : "Status" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif ('loginname' not in request.data or not request.data['loginname']) and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "Username" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif ('email' not in request.data or not request.data['email']) and request.data['status'] != 3:  
            return Response({"status":error.context['error_code'],"message" : "Email" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif ('first_name' not in request.data or not request.data['first_name']) and request.data['status'] != 3:  
            return Response({"status":error.context['error_code'],"message" : "First name" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)  
        elif ('last_name' not in request.data or not request.data['last_name']) and request.data['status'] != 3:  
            return Response({"status":error.context['error_code'],"message" : "Last name" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif ('password' not in request.data or not request.data['password']) and request.data['status'] != 3 and request.data['id'] == '':  
            return Response({"status":error.context['error_code'],"message" : "Password" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        # elif ('desig' not in request.data or not request.data['desig']) and request.data['status'] != 3:  
        #     return Response({"status":error.context['error_code'],"message" : "Desgnations" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)

        elif ('design' not in request.data or not request.data['design']) and request.data['status'] != 3:  
            return Response({"status":error.context['error_code'],"message" : "Desgnations" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)

        elif ('user_role_id' not in request.data or not request.data['user_role_id']) and request.data['status'] != 3:  
            return Response({"status":error.context['error_code'],"message" : "User role" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        # elif ('data_access' not in request.data or not request.data['data_access']) and request.data['status'] != 3:  
        #     return Response({"status":error.context['error_code'],"message" : "Data access" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)                 
        else:
             try:
                # DELETE OPERATION
                if (request.data['status']==3 and request.data['id']!=''):
                    User.objects.filter(id=request.data['id']).update(status=3)
                    #User.objects.filter(id=request.data['id']).delete()
                    return Response({"status":error.context['success_code'],"message" : "User deleted successfully"},status=status.HTTP_200_OK)

                # UPDATE OPERATION
                if 'id' in request.data and request.data['id']!='' and request.data['id'] is not None:
                    user=(User.objects.filter(id=request.data['id']).first())
                    # print(request.data['password'])
                    # user.set_password(request.data['password'])
                    # user.save()

                    # Old ************
                    # User.objects.filter(id=request.data['id']).update(loginname=request.data['loginname'],email=request.data['email'],first_name=request.data['first_name'],last_name=request.data['last_name'],desig=request.data['desig'])

                    User.objects.filter(id=request.data['id']).update(loginname=request.data['loginname'],email=request.data['email'],first_name=request.data['first_name'],last_name=request.data['last_name'],design=request.data['design'])

                    # User.objects.filter(id=request.data['id']).update(loginname=request.data['loginname'],email=request.data['email'],first_name=request.data['first_name'],last_name=request.data['last_name'],process_id=request.data['process'],department_id=request.data['department'], desig=request.data['desig'])
                    if request.data['user_role_id']:
                        UserRoleMapping.objects.filter(user_id=request.data['id']).delete()
                        # for user_role in request.data['user_role_id']:
                        #     UserRoleMapping(user_id=request.data['id'],user_role_id=user_role).save()
                        UserRoleMapping(user_id=request.data['id'],user_role_id=request.data['user_role_id']).save()
                    # if request.data['data_access']:
                    #     DataAccess.objects.filter(user_id=request.data['id']).delete()
                    #     for access in (request.data['data_access']):
                    #         if 'module_id' in access and 'sub_module_id' in access:
                    #             dataAccessSerializer=DataAccessSerializerCRUD(data={"user":request.data['id'],"module":access['module_id']})
                    #             if dataAccessSerializer.is_valid():
                    #                 dataAccessSerializer.save()
                    #                 data_access_id=dataAccessSerializer.data['id']
                    #                 if 'sub_module_id' in access:
                    #                      for sub_module in access['sub_module_id']:
                    #                         DataAccessSubModule.objects.create(data_access_id=data_access_id,sub_module_id=sub_module)

                    if request.data['data_access']:
                        transactionModels.DataAccessForms.objects.filter(user_id=request.data['id']).delete()
                        for access in (request.data['data_access']):
                            if 'form_id' in access:
                                transactionModels.DataAccessForms.objects.create(**{"form_id":access['form_id'],"user_id":request.data['id']})



                    return Response({"status":error.context['success_code'],"message" : "User updated successfully"},status=status.HTTP_200_OK)
                else:
                    # INSERT OPERATION
                    saveserialize=Userserializer(data=request.data)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        user=(User.objects.filter(id=saveserialize.data['id']).first())
                        user.set_password(request.data['password'])
                        user.save()

                        if request.data['user_role_id']:
                            UserRoleMapping.objects.filter(user_id=saveserialize.data['id']).delete()
                            #for user_role in request.data['user_role_id']:
                            #    UserRoleMapping(user_id=saveserialize.data['id'],user_role_id=user_role).save()

                            UserRoleMapping(user_id=saveserialize.data['id'],user_role_id=request.data['user_role_id']).save()
                        # if request.data['data_access']:
                        #     DataAccess.objects.filter(user_id=saveserialize.data['id']).delete()
                        #     for access in (request.data['data_access']):
                        #         if 'module_id' in access and 'sub_module_id' in access:
                        #             #for sub_module in access['sub_module_id']:
                        #             dataAccessSerializer=DataAccessSerializerCRUD(data={"user":saveserialize.data['id'],"module":access['module_id']})
                        #             if dataAccessSerializer.is_valid():
                        #                 dataAccessSerializer.save()
                        #                 data_access_id=dataAccessSerializer.data['id']
                        #                 if 'sub_module_id' in access:
                        #                     #print(access['sub_module_id'], "FFFFFFFFF")
                        #                     for sub_module in access['sub_module_id']:
                        #                         DataAccessSubModule.objects.create(data_access_id=data_access_id,sub_module_id=sub_module)
                                                
                        #             else:
                        #                 return Response({"status" :error.context['error_code'],"message":error.serializerError(dataAccessSerializer)}, status = status.HTTP_200_OK)

                        if request.data['data_access']:
                            transactionModels.DataAccessForms.objects.filter(user_id=saveserialize.data['id']).delete()
                            for access in (request.data['data_access']):
                                if 'form_id' in access:
                                    transactionModels.DataAccessForms.objects.create(**{"form_id":access['form_id'],"user_id":saveserialize.data['id']})

                        return Response({"status" : error.context['success_code'], "message":"New user" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status=status.HTTP_200_OK)
             except:
               return Response({"status":error.context['error_code'],"message" : "Failed to perform this action"},status=status.HTTP_200_OK)



class userImport(APIView):
  
    def post(self,request, pk = None):

            request_file = request.data['user_import']
            dir_storage='static/import_excel'
            fs = FileSystemStorage(location=dir_storage)
            filename = fs.save(request_file.name, request_file)
            if os.path.splitext(request_file.name)[1] == ".xls" or  os.path.splitext(request_file.name)[1] == ".xlsx"or  os.path.splitext(request_file.name)[1] == ".csv":
                excel_folder = os.path.join(settings.BASE_DIR, 'static/import_excel/')
                # print("cvsdd",request_file)
                # read_file = pd.read_csv(request_file,delim_whitespace=True)
               
                # print("cvs",read_file)
                # read_file(excel_folder +'import_excel_file.csv')
                # print("hlo",excel_folder+filename)
                fhand = open(excel_folder+filename)
            else:
                return Response({"status":error.context['error_code'],"message" : "File format not supported (Xls and Xlsx only allowed)" })    
            reader = csv.reader(fhand) 
            next(reader)
            request_data = dict()
            if reader: 
                for row in reader:

                    created_ip  = Common.get_client_ip(request)
                    created_by  = int(request.user.id)

                    #print(created_by,"UUUUUUUUU")

                    count = Designation.objects.values('name').filter(name = row[4]).exclude(status=3).count()

                    if count > 0:
                        id = Designation.objects.values('id').filter(name = row[4]).exclude(status=3)
                        desig_id = id
                    else:
                        # master_designation = {
                        #     'name': row[4],
                        #     'code' : row[4].upper(),
                        #     'created_ip': created_ip,
                        #     'created_by': created_by
                        # }

                        # saveserializelog = DesignationSerializer(data = master_designation)
                        # if saveserializelog.is_valid():
                        #     saveserializelog.save()
                        #     desig_id = saveserializelog.data['id']

                        Designation.objects.create(
                            name = row[4],
                            code = row[4].upper(),
                            status = 1,
                            created_ip = created_ip,
                            #created_by = int(created_by)
                            )

                        id = Designation.objects.values('id').filter(name = row[4]).exclude(status=3)
                        desig_id = id


                    user = User.objects.create(
                            first_name = row[1],
                            last_name = row[2],
                            loginname = row[3],
                            desig_id = desig_id,
                            email = row[5],
                            )

                return Response({"status":error.context['success_code'],"message" : "User imported successfully"})


class userListHierarchy1(APIView):
    def get(self, request, pk = None):       
        filter_values = dict(request.GET.items())
        search_string=order_type=order_column=limit_start=limit_end=''
        normal_values=dict()
        array_values=dict()
        if filter_values:
            for key,values in filter_values.items():
                if values.find("[") !=-1 and values.find("]") !=-1:
                    res = values.strip('][').split(',')
                    array_values[key]=(res)
                else:
                    normal_values[key]=(values)

            strings = ['first_name','last_name']
            search_string = dict((k, normal_values[k]) for k in strings
                                            if k in normal_values)  
            order_column =  request.GET.get('order_column')
            order_type = request.GET.get('order_type')  
            limit_start = request.GET.get('limit_start')
            limit_end = request.GET.get('limit_end')  


            if order_column is not None:                                      
                normal_values.pop('order_column')
            if order_type is not None: 
                normal_values.pop('order_type')  
            if limit_start is not None: 
                normal_values.pop('limit_start')
            if limit_end is not None: 
                normal_values.pop('limit_end')     

            for key in strings:
                if key in normal_values:
                    normal_values.pop(key)

            if search_string:       
                filter_string = None
                for field in search_string:
                    q = Q(**{"%s__contains" % field: search_string[field] })
                    if filter_string:
                        filter_string = filter_string & q
                    else:
                        filter_string = q
        try:
            if pk:
                list = User.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = UserListHierarchySerializer(list)
                return Response({"status":error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except User.DoesNotExist:
            return Response({"status" :error.context['error_code'], "message":"User" +language.context[language.defaultLang]['dataNotFound']}, status = status.HTTP_200_OK)

        lists = User.objects.exclude(status=3)
        if normal_values:
            lists = lists.filter(reduce(operator.and_, 
                               (Q(**d) for d in [dict([i]) for i in normal_values.items()])))
        if array_values:
            for key,values in array_values.items():
                queries= [Q(**{"%s__contains" % key: value }) for value in values]
                query=queries.pop()
                for item in queries:
                    query |= item
                lists = lists.filter(query)

        if search_string:
            lists = lists.filter(filter_string)

        if order_type is None: 
            if order_column:
                lists = lists.order_by(order_column)  

        elif order_type in 'asc':
            if order_column:
                lists = lists.order_by(order_column)
            else: 
                lists = lists.order_by('id')   

        elif order_type in 'desc':
            if order_column:
                order_column = '-' + str(order_column)
                lists = lists.order_by(order_column)
            else: 
                lists = lists.order_by('-id') 

        if limit_start and limit_end:
                lists = lists[int(limit_start):int(limit_end)]

        elif limit_start:
                lists = lists[int(limit_start):]

        elif limit_end:
                lists = lists[0:int(limit_end)]           
        
        serializer = UserListHierarchySerializer(lists, many=True)
        return Response({"status":error.context['success_code'], "data": serializer.data}, status=status.HTTP_200_OK)


class userListHierarchy(APIView):
    def get(self, request, pk = None):

        if 'form_id' in request.GET:

            response = {}

            form_id = request.GET['form_id']

            # Recommender.
            roleList = UserRoleMapping.objects.values('user_id').filter(user_role_id=3)
            role_ids = [role['user_id'] for role in roleList]

            formList = transactionModels.DataAccessForms.objects.values('id','user_id').filter(user_id__in=role_ids, form_id=form_id)
            formList_ids = [form['user_id'] for form in formList]

            response['user_recommender'] = User.objects.values('id','loginname').filter(id__in=formList_ids, status=1).order_by('loginname')


            # Approver.
            approver_roleList = UserRoleMapping.objects.values('user_id').filter(user_role_id=4)
            approver_role_ids = [role['user_id'] for role in approver_roleList]

            approver_formList = transactionModels.DataAccessForms.objects.values('id','user_id').filter(user_id__in=approver_role_ids, form_id=form_id)
            approver_formList_ids = [form['user_id'] for form in approver_formList]
            
            response['user_approver'] = User.objects.values('id','loginname').filter(id__in=approver_formList_ids, status=1).order_by('loginname')

            return Response({"status":error.context['success_code'], "data": response}, status=status.HTTP_200_OK)