from functools import partial
from queue import Empty
from unicodedata import name
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
#from rest_framework import authentication, AllowAny
#from rest_framework.permissions import Is_Authenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import Http404
from functools import reduce
import operator
from django.db.models import Q

from .models import Countries, States, Cities,LookupType,Lookup,Region,Dockyard,Command

from .serializer import Citiesserializer, Countriesserializer, ListCitiesserializer, Statesserializer,ListStatesserializer,LookupTypeSerializer,ListLookupSerializer,LookupSerializer,Regionserializer,ListRegionserializer,CommandSerializer,ListCommandSerializer,DockyardSerializer,ListDockyardSerializer


from transaction import models as transactionModels

from NavyTrials import language,error
from access.views import Common
from django.db.models import Count

from . import models
from . import serializer as cSerializer
import pandas as pd
import os
import csv
from django.core.files.storage import FileSystemStorage
from NavyTrials import language,error,settings,common
# from Glosys import error
           
class CountriesViews(APIView):
    
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

            strings = ['name','description']
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
                list = Countries.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = Countriesserializer(list)
                return Response({"status":error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except Countries.DoesNotExist:
            return Response({"status" :error.context['error_code'], "message":"Country" +language.context[language.defaultLang]['dataNotFound']}, status = status.HTTP_200_OK)

        lists = Countries.objects.exclude(status='3')
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
        
        serializer = Countriesserializer(lists, many=True)
        return Response({"status":error.context['success_code'], "data": serializer.data}, status=status.HTTP_200_OK)

class CountriesDetailViews(APIView):

    

    def get_object(self, pk):
        
            try:
                return Countries.objects.get(pk = pk)
            except Countries.DoesNotExist:
                raise Http404

    
    def post(self,request, pk = None):
        data1=Countries.objects.all()

        # if not name in data1:
        #     return Response({"status" :error.context['error_code'],"message":"name"+language.context[language.defaultLang]['required'] }, status=status.HTTP_200_OK)
        # else:

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "Name" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:  
            return Response({"status":error.context['error_code'],"message" : "code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif 'phone_code' not in request.data and request.data['status'] != 3:  
            return Response({"status":error.context['error_code'],"message" : "phone_code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)  
        elif 'currency' not in request.data and request.data['status'] != 3:  
            return Response({"status":error.context['error_code'],"message" : "Currency" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)                   
        else:
            
            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
                
            if 'id' in request.data:
                pk = request.data['id']  
                created_ip = Common.get_client_ip(request)                                       
                request.data['created_ip'] = created_ip 
                                
                if not pk:
                   
                    duplicate_code = Countries.objects.values('code').filter(code=request.data['code']).exclude(status=3)

                    duplicate_name = Countries.objects.values('name').filter(name=request.data['name']).exclude(status=3)

                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] }, status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] }, status=status.HTTP_200_OK)                    
                    
                    else:

                        saveserialize = Countriesserializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" : error.context['success_code'], "message":"New country" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status=status.HTTP_200_OK)
            
                else:
                    if request.data['status'] != 3:
                        duplicate_code = Countries.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = Countries.objects.values('id','name','status').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            
                    
                    
                    list = self.get_object(pk)

                    saveserialize = Countriesserializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Country" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'],"message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)                         
                   
class StatesViews(APIView):
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

            strings = ['name','description']
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
                list = States.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = ListStatesserializer(list)
                return Response({"status":error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except States.DoesNotExist:
            return Response({"status" :error.context['error_code'], "message":"State" +language.context[language.defaultLang]['dataNotFound']}, status = status.HTTP_200_OK)

        lists = States.objects.exclude(status='3')
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

        serializer = ListStatesserializer(lists, many=True)
        return Response({"status": error.context['success_code'], "data": serializer.data}, status=status.HTTP_200_OK)

class StatesDetailViews(APIView):

    def get_object(self,pk):

        try:
            return States.objects.get(pk = pk)
        except States.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):
             
        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif 'country' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Country" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif 'region' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Region" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)    
        else:

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)                                       
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = States.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = States.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = Statesserializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New state" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = States.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = States.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = Statesserializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"State" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)   

class CityViews(APIView):

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

            strings = ['name','description']
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
                list = Cities.objects.filter(pk=pk).exclude(status='3').get()
                serialize = ListCitiesserializer(list)
                return Response({"status":error.context['success_code'], "data": serialize.data}, status=status.HTTP_200_OK)

        except Cities.DoesNotExist:

            return Response({"status" :error.context['error_code'], "message":"City" +language.context[language.defaultLang]['dataNotFound']}, status = status.HTTP_200_OK)

        lists = Cities.objects.exclude(status='3')
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
      
        serializer = ListCitiesserializer(lists, many=True)
        return Response({"status":error.context['success_code'], "data": serializer.data}, status=status.HTTP_200_OK) 

class CityDetailViews(APIView):

    def get_object(self, pk):

        try:
            return Cities.objects.get(pk=pk)

        except Cities.DoesNotExist:
            #return Response(status=status.HTTP_404_NOT_FOUND)
            raise Http404

            
    def post(self,request,pk=None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "code" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'state' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "State" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)                                       
                request.data['created_ip'] = created_ip  
                
                if not pk:  

                    duplicate_code = Cities.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = Cities.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                 
                        saveserialize = Citiesserializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'],"message":"New city" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)    
                else: 

                    if request.data['status'] != 3:
                        duplicate_code = Cities.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))

                        duplicate_name = Cities.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            


                    list = self.get_object(pk)
                    saveserialize = Citiesserializer(list,data = request.data, partial=True)

                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'],"message":"City" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)

                    else:
                        return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK) 

            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)

class RegionViews(APIView):

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

            strings = ['name','description']
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
                list = Region.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = ListRegionserializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except Region.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Region" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = Region.objects.exclude(status='3')
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
    
        serializer = ListRegionserializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)

class RegionDetailViews(APIView):

    def get_object(self,pk):

        try:
            return Region.objects.get(pk = pk)
        except Region.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif 'country' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Country" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)                                       
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = Region.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = Region.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = Regionserializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New region" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = Region.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = Region.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = Regionserializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Region" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)   

class LookupTypeViews(APIView):

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

            strings = ['name','description']
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
                list = LookupType.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = LookupTypeSerializer(list)
                return Response({"status":error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)

        except LookupType.DoesNotExist:

            return Response({"status" : error.context['error_code'],"message":"Lookup Type"+language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = LookupType.objects.exclude(status='3')
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
            
    
        serializer = LookupTypeSerializer(lists, many=True)
        return Response({"status": error.context['success_code'], "data": serializer.data}, status=status.HTTP_200_OK)
        
class LookupTypeDetailViews(APIView):        
    def get_object(self, pk):
        try:
            return LookupType.objects.get(pk=pk)

        except LookupType.DoesNotExist:
            raise Http404

    def post(self,request,pk=None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status": error.context['error_code'], "message" : "Name"+language.context[language.defaultLang]['missing']  },status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status": error.context['error_code'], "message" : "Code"+language.context[language.defaultLang]['missing']  },status=status.HTTP_200_OK)
        elif 'description' not in request.data and request.data['status'] != 3:
            return Response({"status": error.context['error_code'], "message" : "Description"+language.context[language.defaultLang]['missing']  },status=status.HTTP_200_OK)
        else:
            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)                                       
                request.data['created_ip'] = created_ip 
               

                if not pk:

                    duplicate_code = LookupType.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = LookupType.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'],"message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'],"message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:

                        saveserialize = LookupTypeSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'],"message": "New lookup type"+language.context[language.defaultLang]['insert'] , "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" : error.context['error_code'],"message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)
            
                else: 

                    if request.data['status'] != 3:

                        duplicate_code = LookupType.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = LookupType.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'],"message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'],"message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                   

                    list = self.get_object(pk)
                    saveserialize = LookupTypeSerializer(list, data = request.data,partial=True)

                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'],"message": "Lookup Type"+language.context[language.defaultLang]['update'] , "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" : error.context['error_code'],"message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id'+language.context[language.defaultLang]['missing'] ]}}, status=status.HTTP_200_OK)                  

class LookupViews(APIView):
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

            strings = ['name','description']
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
                list = Lookup.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = ListLookupSerializer(list)
                return Response({"status":error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)

        except Lookup.DoesNotExist:

            return Response({"status" :error.context['error_code'],"message":"Lookup value"+language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = Lookup.objects.exclude(status='3')
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
            
    
        serializer = ListLookupSerializer(lists, many=True)
        return Response({"status": error.context['success_code'], "data": serializer.data}, status=status.HTTP_200_OK)
        

class LookupDetailViews(APIView):
        
    def get_object(self, pk):
        try:
            return Lookup.objects.get(pk=pk)

        except Lookup.DoesNotExist:
            raise Http404

    def post(self,request,pk=None):

        if 'type' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "Type"+language.context[language.defaultLang]['missing']  },status=status.HTTP_200_OK)
        elif 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "Name"+language.context[language.defaultLang]['missing']  },status=status.HTTP_200_OK)    
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "Code"+language.context[language.defaultLang]['missing']  },status=status.HTTP_200_OK)    
        elif 'description' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "Description"+language.context[language.defaultLang]['missing']  },status=status.HTTP_200_OK)    

        else:
            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)                                       
                request.data['created_ip'] = created_ip 
              

                if not pk:

                    duplicate_code = Lookup.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = Lookup.objects.values('name').filter(name=request.data['name']).exclude(status=3)                           
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'],"message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'],"message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                                                                                 
                    else:

                        saveserialize = LookupSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'],"message": "New lookup value"+language.context[language.defaultLang]['insert'] , "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" : error.context['error_code'],"message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)
            
                else: 

                    if request.data['status'] != 3:

                        duplicate_code = Lookup.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))   
                        duplicate_name = Lookup.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))                    
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'],"message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)

                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'],"message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                                                           

                    list = self.get_object(pk)
                    saveserialize = LookupSerializer(list, data = request.data,partial=True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'],"message": "Lookup value"+language.context[language.defaultLang]['update'] , "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'],"message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id'+language.context[language.defaultLang]['missing'] ]}}, status=status.HTTP_200_OK)   



class ProjectViews(APIView):

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

            strings = ['name','description']
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
                list = models.Project.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListProjectSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.Project.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Region" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.Project.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListProjectSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)

class ProjectDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.Project.objects.get(pk = pk)
        except Region.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)                                       
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.Project.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.Project.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.projectSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New project" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.Project.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models.Project.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.projectSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Project" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)   



class ProjectTypeViews(APIView):

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

            strings = ['name','description']
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
                list = models.Project.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListProjectSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.ProjectType.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Region" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.ProjectType.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListProjectTypeSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)

class ProjectTypeDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.ProjectType.objects.get(pk = pk)
        except Region.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)                                       
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.ProjectType.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.ProjectType.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.ProjectTypeSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New project type" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.ProjectType.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models.ProjectType.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.ProjectTypeSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Project type" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)


class CommandViews(APIView):

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

            strings = ['code','name']
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
                list = models.Command.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListCommandSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.Command.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Command" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.Command.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListCommandSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)


class CommandDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.Command.objects.get(pk = pk)
        except Command.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.Command.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.Command.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.CommandSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New Command" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.Command.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models.Command.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.CommandSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Command" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)



class DepartmentViews(APIView):

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

            strings = ['code','name']
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
                list = models.Department.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListDepartmentSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.Department.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Department" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.Department.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListDepartmentSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)


class DepartmentDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.Department.objects.get(pk = pk)
        except Department.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.Department.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.Department.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.DepartmentSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New Department" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.Department.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models.Department.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.DepartmentSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Department" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)


class SectionViews(APIView):

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

            strings = ['code','name']
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
                list = models.Section.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListSectionSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.Section.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Section" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.Section.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListSectionSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)


class SectionDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.Section.objects.get(pk = pk)
        except Section.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.Section.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.Section.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.SectionSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New Section" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.Section.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models.Section.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.SectionSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Section" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)


class SubSectionViews(APIView):

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

            strings = ['code','name']
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
                list = models.SubSection.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListSubSectionSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.SubSection.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"SubSection" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.SubSection.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListSubSectionSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)


class SubSectionDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.SubSection.objects.get(pk = pk)
        except SubSection.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.SubSection.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.SubSection.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.SubSectionSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New SubSection" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.SubSection.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models.SubSection.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.SubSectionSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"SubSection" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)


class UnitTypeViews(APIView):

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

            strings = ['code','name']
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
                list = models.UnitType.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListUnitTypeSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.UnitType.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"UnitType" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.UnitType.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListUnitTypeSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)


class UnitTypeDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.UnitType.objects.get(pk = pk)
        except UnitType.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.UnitType.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.UnitType.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.UnitTypeSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New UnitType" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.UnitType.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models.UnitType.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.UnitTypeSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"UnitType" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)


class UnitViews(APIView):

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

            strings = ['code','name']
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
                list = models.Unit.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListUnitSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.Unit.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Unit" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.Unit.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListUnitSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)


class UnitDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.Unit.objects.get(pk = pk)
        except Unit.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.Unit.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.Unit.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.UnitSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New Unit" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.Unit.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models.Unit.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.UnitSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Unit" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)


class AuthorityViews(APIView):

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

            strings = ['code','name']
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
                list = models.Authority.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListAuthoritySerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.Authority.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Authority" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.Authority.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListAuthoritySerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)


class AuthorityDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.Authority.objects.get(pk = pk)
        except Authority.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.Authority.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.Authority.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.AuthoritySerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New Authority" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.Authority.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models.Authority.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.AuthoritySerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Authority" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)


class ClassViews(APIView):

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

            strings = ['code','name']
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
                list = models.Class.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListClassSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.Class.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Class" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.Class.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListClassSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)


class ClassDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.Class.objects.get(pk = pk)
        except Class.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.Class.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.Class.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.ClassSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New Class" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.Class.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models.Class.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.ClassSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Class" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)

#list
class DockyardViews(APIView):


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

            strings = ['code','name']
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
                list = models.Dockyard.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListDockyardSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.Dockyard.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Dockyard" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.Dockyard.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListDockyardSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)

#crud
class DockyardDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models. Dockyard.objects.get(pk = pk)
        except  Dockyard.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):
        print(request.data,"GGGGGGGGGGGGG")

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models. Dockyard.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models. Dockyard.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.DockyardSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New  Dockyard" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models. Dockyard.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models. Dockyard.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer. DockyardSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Dockyard" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)





class ShipViews(APIView):

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

            strings = ['code','name']
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
                list = models.Ship.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListShipSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.Ship.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Ship" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.Ship.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListShipSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)
        


class ShipDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.Ship.objects.get(pk = pk)
        except Ship.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.Ship.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.Ship.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.ShipSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New Ship" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.Ship.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models.Ship.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.ShipSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Ship" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)


#### Ships

class ShipsViews(APIView):

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

            strings = ['code','name']
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
                list = models.Ships.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListShipSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.Ships.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Ship" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.Ships.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListShipsSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)


class ShipsDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.Ships.objects.get(pk = pk)
        except Ship.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.Ships.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.Ships.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.ShipsSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New Ship" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.Ships.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models.Ships.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.ShipsSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Ship" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)

####


class CompartmentViews(APIView):

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

            strings = ['code','name']
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
                list = models.Compartment.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListCompartmentSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.Compartment.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Compartment" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.Compartment.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListCompartmentSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)


class CompartmentDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.Compartment.objects.get(pk = pk)
        except Compartment.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.Compartment.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.Compartment.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.CompartmentSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New Compartment" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.Compartment.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models.Compartment.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.CompartmentSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Compartment" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)


class SystemViews(APIView):

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

            strings = ['code','name']
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
                list = models.System.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListSystemSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.System.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"System" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.System.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListSystemSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)


class SystemDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.System.objects.get(pk = pk)
        except System.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.System.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.System.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.SystemSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New System" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.System.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models.System.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.SystemSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"System" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)


class EquipmentViews(APIView):

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

            strings = ['code','name']
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
                list = models.Equipment.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListEquipmentSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.Equipment.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Equipment" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.Equipment.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListEquipmentSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)


class EquipmentDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.Equipment.objects.get(pk = pk)
        except Equipment.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.Equipment.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.Equipment.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.EquipmentSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New Equipment" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.Equipment.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models.Equipment.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.EquipmentSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Equipment" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)


class GlobalStatusViews(APIView):

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

            strings = ['code','name']
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
                list = models.GlobalStatus.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListGlobalStatusSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.GlobalStatus.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Status" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.GlobalStatus.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListGlobalStatusSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)


class GlobalStatusDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.GlobalStatus.objects.get(pk = pk)
        except GlobalStatus.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.GlobalStatus.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.GlobalStatus.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.GlobalStatusSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New Status" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.GlobalStatus.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models.GlobalStatus.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.GlobalStatusSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Status" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)


class DesignationViews(APIView):

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

            strings = ['code','name']
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
                list = models.Designation.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListDesignationSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.Designation.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Status" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.Designation.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListDesignationSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)


class DesignationDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.Designation.objects.get(pk = pk)
        except Designation.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.Designation.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.Designation.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.DesignationSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New Designation" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.Designation.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models.Designation.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.DesignationSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Designation" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)


# Global Section
class GlobalSectionViews(APIView):

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

            strings = ['code','name']
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
                list = models.GlobalSection.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListGlobalSectionSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.GlobalSection.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Global Section" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.GlobalSection.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListGlobalSectionSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)


class GlobalSectionDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.GlobalSection.objects.get(pk = pk)
        except GlobalSection.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.GlobalSection.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.GlobalSection.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)            
                    
                    elif duplicate_name:   
                         return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.GlobalSectionSerializer(data = request.data)
                        #print(saveserialize.queries,"FFFFFFFF")
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New Global Section" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.GlobalSection.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models.GlobalSection.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)
                        elif duplicate_name:   
                             return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.GlobalSectionSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Global Section" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)


class GlobalSubSectionViews(APIView):

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

            strings = ['code','name']
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
                list = models.GlobalSubSection.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListGlobalSubSectionSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.GlobalSubSection.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Global SubSection" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.GlobalSubSection.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListGlobalSubSectionSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)


class GlobalSubSectionDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.GlobalSubSection.objects.get(pk = pk)
        except GlobalSubSection.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        # if 'name' not in request.data and request.data['status'] != 3:
        #     return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        if 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.GlobalSubSection.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    #duplicate_name = models.GlobalSubSection.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    #elif duplicate_name:   
                        #return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.GlobalSubSectionSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New Global SubSection" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.GlobalSubSection.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                       # duplicate_name = models.GlobalSubSection.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        #elif duplicate_name:   
                            #return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.GlobalSubSectionSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Global SubSection" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)


class GlobalSubSubSectionViews(APIView):

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

            strings = ['code','name']
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
                list = models.GlobalSubSubSection.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListGlobalSubSubSectionSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.GlobalSubSubSection.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Global SubSubSection" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.GlobalSubSubSection.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListGlobalSubSubSectionSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)


class GlobalSubSubSectionDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.GlobalSubSubSection.objects.get(pk = pk)
        except GlobalSubSubSection.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        # if 'name' not in request.data and request.data['status'] != 3:
        #     return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        if 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.GlobalSubSubSection.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    #duplicate_name = models.GlobalSubSubSection.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    #elif duplicate_name:   
                        #return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.GlobalSubSubSectionSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New Global SubSubSection" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.GlobalSubSubSection.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                       # duplicate_name = models.GlobalSubSubSection.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        #elif duplicate_name:   
                            #return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.GlobalSubSubSectionSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Global SubSubSection" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)




########

class ModuleViews(APIView):

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

            strings = ['code','name']
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
                list = models.Module.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListModuleSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.Module.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Module" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.Module.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListModuleSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)


class ModuleDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.Module.objects.get(pk = pk)
        except Module.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        # elif 'code' not in request.data and request.data['status'] != 3:
        #     return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            # if 'code' in request.data:
            #     request.data['code']=(request.data['code']).upper()
            # if 'sequence' in request.data:
            #     request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    #duplicate_code = models.Module.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.Module.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    # if duplicate_code:            
                    #     return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)            
                    
                    if duplicate_name:   
                         return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.ModuleSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New Module" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        #duplicate_code = models.Module.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models.Module.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        # if duplicate_code:            
                        #     return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)
                        if duplicate_name:   
                             return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.ModuleSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Module" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)



class SubModuleViews(APIView):

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

            strings = ['code','name']
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
                list = models.SubModule.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListSubModuleSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.SubModule.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"SubModule" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.SubModule.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListSubModuleSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)


class SubModuleDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.SubModule.objects.get(pk = pk)
        except SubModule.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        else: 

            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_name = models.SubModule.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                    
                    if duplicate_name:   
                         return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.SubModuleSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New Sub Module" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_name = models.SubModule.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_name:   
                             return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.SubModuleSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Sub Module" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)



class TemplateViews(APIView):

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

            strings = ['code','name']
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
                list = models.Template.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListTemplateSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.Template.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Section" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.Template.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListTemplateSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)


class TemplateDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.Template.objects.get(pk = pk)
        except Template.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            # if 'sequence' in request.data:
            #     request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.Template.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.Template.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)            
                    
                    elif duplicate_name:   
                         return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.TemplateSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New Section" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.Template.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models.Template.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)
                        elif duplicate_name:   
                             return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.TemplateSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Section" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)


class TemplateConfigViews(APIView):

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

            strings = ['code','name']
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
                list = models.TemplateConfig.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListTemplateConfigSerializer2(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.TemplateConfig.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Section" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.TemplateConfig.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListTemplateConfigSerializer2(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)


class TemplateConfigDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.TemplateConfig.objects.get(pk = pk)
        except models.TemplateConfig.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        #print(request.data)
        if 'template' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Template" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        else: 
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  


                count = models.TemplateConfigMaster.objects.filter(template_id=request.data['template']).count()
               
                models.TemplateConfigMaster.objects.filter(template_id = request.data['template']).delete()

                #print(pk,"PK")
                pk = None

                if not pk: 
                    master_template = {
                        'template': request.data['template'],
                        'created_ip': created_ip,
                        'created_by': request.data['created_by']
                    }

                    print(master_template,"YYYYY")

                    saveserializelog = cSerializer.TemplateConfigMasterCURDSerializer(data = master_template)
                    if saveserializelog.is_valid():
                        saveserializelog.save()
                        running_id = saveserializelog.data['id']


                    for access in (request.data['data_access']):

                        section_value = None
                        compartment_value = None
                        selection_from = None
                        selection_to = None

                        sub_section_value = None
                        sub_compartment_value = None
                        sub_selection_from = None
                        sub_selection_to = None    
                        
                        sub_sub_section_value = None
                        sub_sub_compartment_value = None
                        sub_sub_selection_from = None
                        sub_sub_selection_to = None
                        #if 'module' in access and 'sub_module' in access:
                        #print(access['module'])

                        if access['section_type']==1:
                            section_value = access['section_value'];
                        if access['section_type']==2:
                            compartment_value = access['compartment_value'];
                        if access['section_type']==3:
                            selection_from = access['selection_from'];
                            selection_to = access['selection_to'];

                        if access['sub_section_type']==1:
                            sub_section_value = access['sub_section_value'];
                        if access['sub_section_type']==2:
                            sub_compartment_value = access['sub_compartment_value'];
                        if access['sub_section_type']==3:
                            sub_selection_from = access['sub_selection_from'];
                            sub_selection_to = access['sub_selection_to'];

                        if access['sub_sub_section_type']==1:
                            sub_sub_section_value = access['sub_sub_section_value'];
                        if access['sub_sub_section_type']==2:
                            sub_sub_compartment_value = access['sub_sub_compartment_value'];
                        if access['sub_sub_section_type']==3:
                            sub_sub_selection_from = access['sub_sub_selection_from'];
                            sub_sub_selection_to = access['sub_sub_selection_to'];

                        saveserialize = cSerializer.TemplateConfigSerializer(data={
                            'template_config_master' : running_id,
                            "template" : request.data['template'],
                            "module" : access['module'],
                            "sub_module" : access['sub_module'],

                            "section_type" : access['section_type'],
                            "section_value" : section_value,
                            "compartment_value" : compartment_value,
                            "selection_from" : selection_from,
                            "selection_to" : selection_to,

                            "sub_section_type" : access['sub_section_type'],
                            "sub_section_value" : sub_section_value,
                            "sub_compartment_value" : sub_compartment_value,
                            "sub_selection_from" : sub_selection_from,
                            "sub_selection_to" : sub_selection_to,

                            "sub_sub_section_type" : access['sub_sub_section_type'],
                            "sub_sub_section_value" : sub_sub_section_value,
                            "sub_sub_compartment_value" : sub_sub_compartment_value,
                            "sub_sub_selection_from" : sub_sub_selection_from,
                            "sub_sub_selection_to" : sub_sub_selection_to,
                            "status" : request.data['status'],
                            "created_ip" : created_ip

                            })

                        if saveserialize.is_valid():
                        
                            saveserialize.save() 
                    

                    if count > 0:    
                        return Response({"status" :error.context['success_code'], "message":"Template config" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['success_code'], "message":"Template config" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)

                    # else:
                    #     return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)


                    # saveserialize = cSerializer.TemplateConfigSerializer(data = request.data)
                    # if saveserialize.is_valid():
                    #     saveserialize.save()
                    #     return Response({"status" :error.context['success_code'], "message":"New template config" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    # else:
                    #     return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    #if request.data['status'] != 3:
                        # duplicate_code = models.TemplateConfig.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        # duplicate_name = models.TemplateConfig.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        # if duplicate_code:            
                        #     return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)
                        # elif duplicate_name:   
                        #      return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.TemplateConfigSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Template config" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)


class TemplateConfigMasterViews(APIView):

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

            strings = ['code','name']
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
                list = models.TemplateConfigMaster.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.TemplateConfigMasterSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.TemplateConfigMaster.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Section" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.TemplateConfigMaster.objects.exclude(status='3')
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
    
        serializer = cSerializer.TemplateConfigMasterSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)


class DeleteTemplateConfigMaster(APIView):

    def post(self,request, pk = None):
        if 'id' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "id" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        else: 
            if models.TemplateConfigMaster.objects.filter(id=request.data['id']).count()>0:
                models.TemplateConfigMaster.objects.filter(id=request.data['id']).update(**{"status":3})
                return Response({"status" :error.context['success_code'], "message":"Template config deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"status" :error.context['error_code'], "message":"Incorrect id supplied in the parameter"}, status=status.HTTP_200_OK)

class GeneratePSRTemplateViews2(APIView):

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

            strings = ['code','name']
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
                list = models.TemplateConfigMaster.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.TemplateConfigMasterSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.TemplateConfigMaster.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Section" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.TemplateConfigMaster.objects.exclude(status='3')
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
    
        serializer = cSerializer.TemplateConfigMasterSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)


class GeneratePSRTemplateViews(APIView):

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

            strings = ['code','name']
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
                list = models.SubModule.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.TemplateGenerateSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.SubModule.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Section" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.SubModule.objects.exclude(status='3')
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
    
        serializer = cSerializer.TemplateGenerateSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)



class getSectionCompartment(APIView):
    authentication_classes = [] #disables authentication
    permission_classes = [] #disables permission
    def post(self,request, pk = None):
        if 'global_section_id' not in request.data or request.data['global_section_id'] == '':
            return Response({"status":error.context['error_code'], "message" : "Global section id " +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        else:
            if request.data['global_sub_section_id'] == '' and request.data['global_sub_sub_section_id'] == '':
                compartment = cSerializer.ListCompartmentSerializer(models.Compartment.objects.filter(global_section_id=request.data['global_section_id'],global_sub_section_id__isnull=True,global_sub_sub_section_id__isnull=True),many=True)

            if request.data['global_section_id'] != '' and request.data['global_sub_section_id'] != '' and request.data['global_sub_sub_section_id'] == '':
                compartment = cSerializer.ListCompartmentSerializer(models.Compartment.objects.filter(global_section_id=request.data['global_section_id'],global_sub_section_id=request.data['global_sub_section_id'],global_sub_sub_section_id__isnull=True),many=True)

            if request.data['global_section_id'] != '' and request.data['global_sub_section_id'] != '' and request.data['global_sub_sub_section_id'] != '':
                compartment = cSerializer.ListCompartmentSerializer(models.Compartment.objects.filter(global_section_id=request.data['global_section_id'],global_sub_section_id=request.data['global_sub_section_id'],global_sub_sub_section_id=request.data['global_sub_sub_section_id']),many=True)

            return Response({"status":error.context['success_code'] , "data": compartment.data}, status=status.HTTP_200_OK)


class getSectionSystem(APIView): 
    authentication_classes = [] #disables authentication
    permission_classes = [] #disables permission
    def post(self,request, pk = None):
        if 'global_section_id' not in request.data or request.data['global_section_id'] == '':
            return Response({"status":error.context['error_code'], "message" : "Global section id " +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        else:
            if request.data['global_sub_section_id'] == '' and request.data['global_sub_sub_section_id'] == '':
                system = cSerializer.ListCompartmentSerializer(models.System.objects.filter(global_section_id=request.data['global_section_id'],global_sub_section_id__isnull=True,global_sub_sub_section_id__isnull=True),many=True)

            if request.data['global_section_id'] != '' and request.data['global_sub_section_id'] != '' and request.data['global_sub_sub_section_id'] == '':
                system = cSerializer.ListSystemSerializer(models.System.objects.filter(global_section_id=request.data['global_section_id'],global_sub_section_id=request.data['global_sub_section_id'],global_sub_sub_section_id__isnull=True),many=True)

            if request.data['global_section_id'] != '' and request.data['global_sub_section_id'] != '' and request.data['global_sub_sub_section_id'] != '':
                system = cSerializer.ListSystemSerializer(models.System.objects.filter(global_section_id=request.data['global_section_id'],global_sub_section_id=request.data['global_sub_section_id'],global_sub_sub_section_id=request.data['global_sub_sub_section_id']),many=True)

            return Response({"status":error.context['success_code'] , "data": system.data}, status=status.HTTP_200_OK)


class getSectionEquipment(APIView): 
    authentication_classes = [] #disables authentication
    permission_classes = [] #disables permission
    def post(self,request, pk = None):
        if 'global_section_id' not in request.data or request.data['global_section_id'] == '':
            return Response({"status":error.context['error_code'], "message" : "Global section id " +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        else:
            if request.data['global_sub_section_id'] == '' and request.data['global_sub_sub_section_id'] == '':
                equipment = cSerializer.ListCompartmentSerializer(models.Equipment.objects.filter(global_section_id=request.data['global_section_id'],global_sub_section_id__isnull=True,global_sub_sub_section_id__isnull=True),many=True)

            if request.data['global_section_id'] != '' and request.data['global_sub_section_id'] != '' and request.data['global_sub_sub_section_id'] == '':
                equipment = cSerializer.ListEquipmentSerializer(models.Equipment.objects.filter(global_section_id=request.data['global_section_id'],global_sub_section_id=request.data['global_sub_section_id'],global_sub_sub_section_id__isnull=True),many=True)

            if request.data['global_section_id'] != '' and request.data['global_sub_section_id'] != '' and request.data['global_sub_sub_section_id'] != '':
                equipment = cSerializer.ListEquipmentSerializer(models.Equipment.objects.filter(global_section_id=request.data['global_section_id'],global_sub_section_id=request.data['global_sub_section_id'],global_sub_sub_section_id=request.data['global_sub_sub_section_id']),many=True)

            return Response({"status":error.context['success_code'] , "data": equipment.data}, status=status.HTTP_200_OK)

### Form Mapping ####

class FormMappingModuleViews(APIView):

    def get(self, request, pk = None):
        lists = models.Module.objects.values('id','name').filter(status='1').order_by('id')
        #print(lists)
        return Response({"status":error.context['success_code'] , "data": lists}, status=status.HTTP_200_OK)

class FormMappingSubModuleViews(APIView):

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

            strings = ['code','name']
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
                list = models.SubModule.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListSubModuleSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.SubModule.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"SubModule" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.SubModule.objects.values('id','name','module_id').exclude(status='3')
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
    
        #serializer = cSerializer.ListSubModuleSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": lists}, status=status.HTTP_200_OK)


class FormMappingGlobalSectionViews(APIView):

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

            strings = ['code','name']
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
                list = models.GlobalSection.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListGlobalSectionSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.GlobalSection.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Global Section" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        #lists = models.GlobalSection.objects.exclude(status='3')
        lists = models.GlobalSection.objects.values('id','name','module_id','sub_module_id').exclude(status='3')
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
    
        #serializer = cSerializer.ListGlobalSectionSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": lists}, status=status.HTTP_200_OK)


class FormMappingGlobalSubSectionViews(APIView):

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

            strings = ['code','name']
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
                list = models.GlobalSubSection.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListGlobalSubSectionSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.GlobalSubSection.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Global SubSection" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        #lists = models.GlobalSubSection.objects.exclude(status='3')
        lists = models.GlobalSubSection.objects.values('id','name','module_id','sub_module_id','global_section_id').exclude(status='3')
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
    
        #serializer = cSerializer.ListGlobalSubSectionSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": lists}, status=status.HTTP_200_OK)


class FormMappingGlobalSubSubSectionViews(APIView):

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

            strings = ['code','name']
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
                list = models.GlobalSubSubSection.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListGlobalSubSubSectionSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.GlobalSubSubSection.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Global SubSubSection" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        #lists = models.GlobalSubSubSection.objects.exclude(status='3')
        lists = models.GlobalSubSubSection.objects.values('id','name','module_id','sub_module_id','global_section_id','global_sub_section_id').exclude(status='3')
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
    
        #serializer = cSerializer.ListGlobalSubSubSectionSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": lists}, status=status.HTTP_200_OK)




### Dockyard ###

class DockyardGroupViews(APIView):


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

            strings = ['code','name']
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
                list = models.DockyardGroup.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListDockyardGroupSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.DockyardGroup.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"DockyardGroup" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.DockyardGroup.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListDockyardGroupSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)

class DockyardGroupDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.DockyardGroup.objects.get(pk = pk)
        except  DockyardGroup.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):
        #print(request.data,"GGGGGGGGGGGGG")

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.DockyardGroup.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.DockyardGroup.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.DockyardGroupSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New dockyard group" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.DockyardGroup.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models. DockyardGroup.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.DockyardGroupSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Dockyard group" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)


class DockyardSubGroupViews(APIView):


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

            strings = ['code','name']
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
                list = models.DockyardSubGroup.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListDockyardSubGroupSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.DockyardSubGroup.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Dockyard sub group" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.DockyardSubGroup.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListDockyardSubGroupSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)

class DockyardSubGroupDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.DockyardSubGroup.objects.get(pk = pk)
        except  DockyardSubGroup.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):
        #print(request.data,"GGGGGGGGGGGGG")

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.DockyardSubGroup.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.DockyardSubGroup.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.DockyardSubGroupSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New dockyard sub group" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.DockyardSubGroup.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models. DockyardSubGroup.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.DockyardSubGroupSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Dockyard sub group" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)




class RefitTypeViews(APIView):

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

            strings = ['name','description']
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
                list = models.RefitType.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListProjectSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.RefitType.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Region" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.RefitType.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListRefitTypeSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)

class RefitTypeDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.RefitType.objects.get(pk = pk)
        except Region.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)                                       
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.RefitType.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.RefitType.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.RefitTypeSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New refit type" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.RefitType.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models.RefitType.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.RefitTypeSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Refit type" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)

class DefectViews(APIView):

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

            strings = ['name','description']
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
                list = models.Defect.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListDefectSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.Defect.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Region" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.Defect.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListDefectSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)

class DefectDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.Defect.objects.get(pk = pk)
        except Defect.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)                                       
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.Defect.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.Defect.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.DefectSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New defect" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.Defect.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models.Defect.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.DefectSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Defect" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)   



class CenterViews(APIView):

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

            strings = ['name','description']
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
                list = models.Center.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListCenterSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.Center.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Center" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.Center.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListCenterSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)

class CenterDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.Center.objects.get(pk = pk)
        except Center.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)                                       
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.Center.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.Center.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.CenterSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New center" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.Center.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models.Center.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.CenterSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Center" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)   



class ShopFloorViews(APIView):

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

            strings = ['name','description']
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
                list = models.Shopfloor.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = cSerializer.ListShopfloorSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except models.Shopfloor.DoesNotExist:
            return Response({"status" : error.context['error_code'], "message":"Shopfloor" +language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = models.Shopfloor.objects.exclude(status='3')
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
    
        serializer = cSerializer.ListShopfloorSerializer(lists, many=True)
        return Response({"status":error.context['success_code'] , "data": serializer.data}, status=status.HTTP_200_OK)

class ShopFloorDetailViews(APIView):

    def get_object(self,pk):

        try:
            return models.Shopfloor.objects.get(pk = pk)
        except Shopfloor.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Name" +language.context[language.defaultLang]['missing']},status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'], "message" : "Code" +language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else: 

            if 'code' in request.data:
                request.data['code']=(request.data['code']).upper()
            if 'sequence' in request.data:
                request.data['sequence']=request.data['sequence'] if(request.data['sequence']!='')  else 0
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)                                       
                request.data['created_ip'] = created_ip  
               
                if not pk: 
                    duplicate_code = models.Shopfloor.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = models.Shopfloor.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    elif duplicate_name:   
                        return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                
                        saveserialize = cSerializer.ShopfloorSerializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'], "message":"New shopfloor" +language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'], "message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:
                    if request.data['status'] != 3:
                        duplicate_code = models.Shopfloor.objects.values('code').filter(code=request.data['code']).exclude(Q(id=request.data['id']) | Q(status=3))
                        duplicate_name = models.Shopfloor.objects.values('name').filter(name=request.data['name']).exclude(Q(id=request.data['id']) | Q(status=3))
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'], "message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                                            

                    list = self.get_object(pk)

                    saveserialize = cSerializer.ShopfloorSerializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'], "message":"Shopfloor" +language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'], "message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else: 
                return Response({"status" : {"id" : ['id' +language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)   



class ImportExcelDefect(APIView):

    def post(self,request, pk = None): 
        
        created_ip = Common.get_client_ip(request)
        request_file = request.FILES['excel_file_upload']
        created_by = request.data['created_by']

        dir_storage='static/import_excel'
        fs = FileSystemStorage(location=dir_storage)
        filename = fs.save(request_file.name, request_file)
        if os.path.splitext(request_file.name)[1] == ".xls" or  os.path.splitext(request_file.name)[1] == ".xlsx":
            excel_folder = os.path.join(settings.BASE_DIR, 'media/Excel/Defect/')
            read_file = pd.read_excel(request_file)
            read_file.to_csv(excel_folder +'import_excel_file.csv')
            fhand = open('media/Excel/Defect/import_excel_file.csv')
        else:
             return Response({"status":error.context['error_code'],"message" : "File format not supported (Xls and Xlsx only allowed)" })    
        reader = csv.reader(fhand)
        next(reader)
        #print(reader)
        
        for row in reader:
            #print(row[1])
            if not request_file:
                return Response({"status":error.context['error_code'],"message" : "Upload file is required" })

            refit_type = models.RefitType.objects.filter(code=row[1]).first()            

            if not refit_type:
                refit_type = None
            else:
                refit_type = refit_type.id

            request_data = {
                'refit_type' : refit_type,
                'name' : row[2],
                'description' : row[3],
                'code' : row[4],
                'dl_1' : row[5],
                'dl_2' : row[6],
                'dl_3' : row[7],
                'sdl' : row[8],
                'awrf_1' : row[9],
                'awrf_2' : row[10],
                'awrf_3' : row[11],
                'status' : 1,
                'created_ip': created_ip,
                'created_by': created_by
            }

            saveserialize = cSerializer.DefectSerializer(data = request_data)
            if saveserialize.is_valid():
                saveserialize.save()

        excel_upload_obj = transactionModels.ExcelFileDefectUpload.objects.create(
        excel_file_upload = request.data['excel_file_upload'],
        created_ip =  created_ip
        )
        
        if excel_upload_obj:
            return Response({"status" :error.context['success_code'], "message":"File imported successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"status" :error.context['error_code'],"message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)


class ImportExcelShip(APIView):

    def post(self,request, pk = None):

        created_ip = Common.get_client_ip(request)
        request_file = request.FILES['excel_file_upload']
        created_by = request.data['created_by']

        dir_storage='static/import_excel'
        fs = FileSystemStorage(location=dir_storage)
        filename = fs.save(request_file.name, request_file)
        if os.path.splitext(request_file.name)[1] == ".xls" or  os.path.splitext(request_file.name)[1] == ".xlsx":
            excel_folder = os.path.join(settings.BASE_DIR, 'media/Excel/Ship/')
            read_file = pd.read_excel(request_file)
            read_file.to_csv(excel_folder +'import_excel_file.csv')
            fhand = open('media/Excel/Ship/import_excel_file.csv')
        else:
             return Response({"status":error.context['error_code'],"message" : "File format not supported (Xls and Xlsx only allowed)" })    
        reader = csv.reader(fhand)
        next(reader)
        #print(reader)

        for row in reader:
            #print(row[1])
            if not request_file:
                return Response({"status":error.context['error_code'],"message" : "Upload file is required" })

            command = models.Command.objects.filter(CommandID=row[5]).first()

            if not command:
                command_id = None
            else:
                command_id = command.id

            request_data = {
                'name' : row[1],
                'ShipID' : row[2],
                'description' : row[3],
                'code' : row[4],
                'command_id' : command_id,
                'status' : 1,
                'created_ip': created_ip,
                'created_by': created_by
            }

            print(request_data,"")

            saveserialize = cSerializer.ShipSerializer(data = request_data)
            if saveserialize.is_valid():
                saveserialize.save()

        excel_upload_obj = transactionModels.ExcelFileShipUpload.objects.create(
        excel_file_upload = request.data['excel_file_upload'],
        created_ip =  created_ip
        )

        if excel_upload_obj:
            return Response({"status" :error.context['success_code'], "message":"File imported successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"status" :error.context['error_code'],"message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)


class ImportExcelEquipment(APIView):

    def post(self,request, pk = None):

        created_ip = Common.get_client_ip(request)
        request_file = request.FILES['excel_file_upload']
        created_by = request.data['created_by']

        dir_storage='static/import_excel'
        fs = FileSystemStorage(location=dir_storage)
        filename = fs.save(request_file.name, request_file)
        if os.path.splitext(request_file.name)[1] == ".xls" or  os.path.splitext(request_file.name)[1] == ".xlsx":
            excel_folder = os.path.join(settings.BASE_DIR, 'media/Excel/Equipment/')
            read_file = pd.read_excel(request_file)
            read_file.to_csv(excel_folder +'import_excel_file.csv')
            fhand = open('media/Excel/Equipment/import_excel_file.csv')
        else:
             return Response({"status":error.context['error_code'],"message" : "File format not supported (Xls and Xlsx only allowed)" })    
        reader = csv.reader(fhand)
        next(reader)
        #print(reader)

        for row in reader:
            #print(row[1])
            #print(type(int(row[10])),"TYYGHHHHV", row[10])
            if not request_file:
                return Response({"status":error.context['error_code'],"message" : "Upload file is required" })

            section = models.Section.objects.filter(code=row[4]).first()
            if row[10]!="":
                ship = models.Ship.objects.filter(ShipID=int(float(row[10]))).first()
            else:
                ship = None

            if not section:
                section_id = None
            else:
                section_id = section.id

            if not ship:
                ship_id = None
            else:
                ship_id = ship.id

            request_data = {
                'EquipmentID' : row[1],
                'code' : row[2],
                'name' : row[3],
                'section_id' : section_id,
                'equipment_model' : row[5],
                'nomenclature' : row[6],
                'equipment_ship_id' : row[7],
                'esd_equipment_id' : row[8],
                'esd_equipment_code' : row[9],
                'ship' : ship_id,
                'universal_id_m_ship' : row[11],
                'equipment_sr_no': row[12],
                'status' : 1,
                'created_ip': created_ip,
                'created_by': created_by
            }


            print(request_data,"GGGGG")

            saveserialize = cSerializer.EquipmentSerializer(data = request_data)
            if saveserialize.is_valid():
                saveserialize.save()
            else:
                return Response({"status" :error.context['error_code'],"message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)

        excel_upload_obj = transactionModels.ExcelFileEquipmentUpload.objects.create(
        excel_file_upload = request.data['excel_file_upload'],
        created_ip =  created_ip
        )

        if excel_upload_obj:
            return Response({"status" :error.context['success_code'], "message":"File imported successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"status" :error.context['error_code'],"message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)