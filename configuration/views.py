from distutils.command.config import config
from django.shortcuts import render

from functools import partial
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import Http404
from functools import reduce
import operator
from django.db.models import Q
from .models import Configurationtable,RoleConfiguration,TemplatesCountry,Templatestable,Approval
from .serializer import Configurationtableserializer,TemplateCountryserializer,ListTemplateCountryserializer,Templatestableserializer,ApprovalSerializer,ApprovalListSerializer
from NavyTrials import language,error
from access.views import Common
from datetime import datetime



class ConfigurationTableViews(APIView):
    
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

            strings = ['name','type']
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
                list = Configurationtable.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = Configurationtableserializer(list)
                return Response({"status":error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except Configurationtable.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message": "configuration"+language.context[language.defaultLang]['dataNotFound']}, status = status.HTTP_200_OK)

        lists = Configurationtable.objects.exclude(status='3')
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

        serializer =Configurationtableserializer (lists, many=True)
        return Response({"status": error.context['success_code'], "data": serializer.data}, status=status.HTTP_200_OK)

class ConfigurationTableDetailViews(APIView):

    def get_object(self,pk):

        try:
            return Configurationtable.objects.get(pk = pk)
        except Configurationtable.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'id' in request.data:
            pk = request.data['id']
                        
            if not pk:
            
                saveserialize = Configurationtableserializer(data = request.data)
               
                if saveserialize.is_valid():
                    saveserialize.save()
                    
                    isCenter = request.data['isCenter']
                    if isCenter:
                       center_id = request.data['center']
                       for id in center_id:
                           configurationtable = CenterConfiguration.objects.create(center_id=id,config_id=saveserialize.data['id'])
                    if request.data['role']:
                        RoleConfiguration.objects.filter(config_id=saveserialize.data['id']).delete()
                        for id in request.data['role']:
                               configurationtable = RoleConfiguration.objects.create(role_id=id,config_id=saveserialize.data['id'])  
                    
                    return Response({"status" : error.context['success_code'], "message": "New configuration"+language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                else:
                    return Response({"status" : error.context['error_code'], "message":str( saveserialize.errors)}, status=status.HTTP_200_OK)

            else:

                list = self.get_object(pk)
                saveserialize = Configurationtableserializer(list, data = request.data, partial= True)
                if saveserialize.is_valid():
                    saveserialize.save()
                    
                    isCenter = request.data['isCenter']
                    if isCenter :
                       center_id = request.data['center']
                       CenterConfiguration.objects.filter(config_id=saveserialize.data['id']).delete()
                       for id in center_id:
                           configurationtable = CenterConfiguration.objects.create(center_id=id,config_id=saveserialize.data['id'])

                    if request.data['role']:
                        RoleConfiguration.objects.filter(config_id=saveserialize.data['id']).delete()
                        for id in request.data['role']:
                               configurationtable = RoleConfiguration.objects.create(role_id=id,config_id=saveserialize.data['id'])  

                    return Response({"status" : error.context['success_code'], "message": " configuration"+language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                else:
                    return Response({"status" : error.context['error_code'], "message":str(saveserialize.errors)}, status = status.HTTP_200_OK)
        else: 
            return Response({"status" : {"id" : ['id'+language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)  



class TemplatetableViews(APIView):
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

            strings = ['actual_tempalte']
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
                list = Templatestable.objects.filter(pk=pk).get()
                serializeobj = Templatestableserializer(list)
                return Response({"status":error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except Templatestable.DoesNotExist:
            return Response({"status" :error.context['error_code'], "message":"Templates table" +language.context[language.defaultLang]['dataNotFound']}, status = status.HTTP_200_OK)

        lists = Templatestable.objects.all()
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

        serializer = Templatestableserializer(lists, many=True)
        return Response({"status": error.context['success_code'], "data": serializer.data}, status=status.HTTP_200_OK)  

class TemplatetableDetailViews(APIView):

    def get_object(self,pk):

        try:
            return Templatestable.objects.get(pk = pk)
        except Templatestable.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'title' not in request.data and 'id' not in request.data:
            return Response({"status":error.context['error_code'], "message" : "title" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)       
        elif 'code' not in request.data and 'id' not in request.data:
            return Response({"status":error.context['error_code'], "message" : "code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif 'actual_template' not in request.data and 'id' not in request.data:
            return Response({"status":error.context['error_code'], "message" : "actual_template" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)    
       
        else:   

            if 'id' in request.data:
                pk = request.data['id']  
                modified_ip = Common.get_client_ip(request)                                       
                request.data['modified_ip'] = modified_ip 

                if not pk: 

                        saveserialize = Templatestableserializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New template " +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": str(saveserialize.errors)}, status=status.HTTP_200_OK)

                else:
                    
                    list = self.get_object(pk)

                    saveserialize = Templatestableserializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Template " +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":str(saveserialize.errors)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)
class TemplateCountryViews(APIView):
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

            strings = ['actual_tempalte']
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
                list = TemplatesCountry.objects.filter(pk=pk).get()
                serializeobj = ListTemplateCountryserializer(list)
                return Response({"status":error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except TemplatesCountry.DoesNotExist:
            return Response({"status" :error.context['error_code'], "message":"Templates country" +language.context[language.defaultLang]['dataNotFound']}, status = status.HTTP_200_OK)

        lists = TemplatesCountry.objects.all()
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

        serializer = ListTemplateCountryserializer(lists, many=True)
        return Response({"status": error.context['success_code'], "data": serializer.data}, status=status.HTTP_200_OK)   

class TemplateCountryDetailViews(APIView):

    def get_object(self,pk):

        try:
            return TemplatesCountry.objects.get(pk = pk)
        except TemplatesCountry.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'template' not in request.data and 'id' not in request.data:
            return Response({"status":error.context['error_code'], "message" : "Template_id" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)       
        elif 'country' not in request.data and 'id' not in request.data:
            return Response({"status":error.context['error_code'], "message" : "Country_id" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
       
        else:   

            if 'id' in request.data:
                pk = request.data['id']  
                modified_ip = Common.get_client_ip(request)                                       
                request.data['modified_ip'] = modified_ip 

                if not pk: 

                        saveserialize = TemplateCountryserializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New template " +language.context[language.defaultLang]['insert']+' with country', "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": str(saveserialize.errors)}, status=status.HTTP_200_OK)

                else:
                    
                    list = self.get_object(pk)

                    saveserialize = TemplateCountryserializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Template " +language.context[language.defaultLang]['update']+' with country', "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":str(saveserialize.errors)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)


class approvalList(APIView):
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

            strings = []
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
                list = Approval.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = ApprovalListSerializer(list)
                return Response({"status":error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except Approval.DoesNotExist:
            return Response({"status" :error.context['error_code'], "message":"User" +language.context[language.defaultLang]['dataNotFound']}, status = status.HTTP_200_OK)

        lists = Approval.objects.exclude(status=3)
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
        
        serializer = ApprovalListSerializer(lists, many=True)
        return Response({"status":error.context['success_code'], "data": serializer.data}, status=status.HTTP_200_OK)

class approvalCRUD(APIView):
    def post(self, request):
        if ('status' not in request.data):
            return Response({"status":error.context['error_code'],"message" : "Status" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif ('trail_unit' not in request.data or not request.data['trail_unit']) and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "Trail unit" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif ('satellite_unit' not in request.data or not request.data['satellite_unit']) and request.data['status'] != 3:  
            return Response({"status":error.context['error_code'],"message" : "Satellite unit" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif ('user_role' not in request.data or not request.data['user_role']) and request.data['status'] != 3:  
            return Response({"status":error.context['error_code'],"message" : "User role" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)  
        elif ('level' not in request.data or not request.data['level']) and request.data['status'] != 3:  
            return Response({"status":error.context['error_code'],"message" : "Level" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else:
            try:
                # DELETE OPERATION
                if (request.data['status']==3 and request.data['id']!=''):
                    Approval.objects.filter(id=request.data['id']).delete()
                    return Response({"status":error.context['success_code'],"message" : "Approval deleted successfully"},status=status.HTTP_200_OK)

                # UPDATE OPERATION
                if 'id' in request.data and request.data['id']!='' and request.data['id'] is not None:
                    print(request.user.id)
                    request.data['modified_by']=request.user.id
                    request.data['modified_ip']=Common.get_client_ip(request)
                    
                    saveserialize = ApprovalSerializer(Approval.objects.get(id=request.data['id']), data = request.data, partial= True)
                    #Approval.objects.filter(id=request.data['id']).update(trail_unit_id=request.data['trail_unit'],satellite_unit_id=request.data['satellite_unit'],user_role_id=request.data['user_role'],level=request.data['level'])
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" : error.context['success_code'], "message":"Approval updated successfully", "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status=status.HTTP_200_OK)
                else:
                    # INSERT OPERATION
                    request.data['created_by']=request.user.id
                    request.data['created_ip']=Common.get_client_ip(request)  
                    print(request.data)
                    saveserialize=ApprovalSerializer(data=request.data)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" : error.context['success_code'], "message":"New approval" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status=status.HTTP_200_OK)
                    return Response({"status":error.context['success_code'],"message" : "Approval created successfully"},status=status.HTTP_200_OK)
            except:
                return Response({"status":error.context['error_code'],"message" : "Failed to perform this action"},status=status.HTTP_200_OK)