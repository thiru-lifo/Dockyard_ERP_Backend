from django.shortcuts import render
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

from .models import UserLogin 
from .serializer import UserLoginserializer

from NavyTrials import language

class UserLoginViews(APIView):
    
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

            strings = ['log_browser','log_version']
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
                list = UserLogin.objects.filter(pk=pk).get()
                serializeobj = UserLoginserializer(list)
                return Response({"status": "success", "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except UserLogin.DoesNotExist:
            return Response({"status" :"error","message":"userlogin"+language.context[language.defaultLang]['dataNotFound']}, status = status.HTTP_400_BAD_REQUEST)

        lists = UserLogin.objects
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

        serializer = UserLoginserializer(lists, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class UserLoginDetailViews(APIView):

    def get_object(self, pk):
        
            try:
                return UserLogin.objects.get(pk = pk)
            except UserLogin.DoesNotExist:
                raise Http404

    
    def post(self,request, pk = None):

        if 'id' in request.data:
            pk = request.data['id']
            if not pk:

                saveserialize = UserLoginserializer(data = request.data)
                if saveserialize.is_valid():
                    saveserialize.save()
                    return Response({"status" : "success","message":"userlogin"+language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                else:
                    return Response({"status" :"error","message": saveserialize.errors}, status=status.HTTP_400_BAD_REQUEST)
        
            else:

                list = self.get_object(pk)
                serializer = UserLoginserializer(list,data=request.data, partial= True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status" :"success","message": "userlogin"+language.context[language.defaultLang]['update'], "data" :serializer.data})
                else:
                    return Response({"status" : "error","message":language.context[language.defaultLang]['invaild data']}, status = status.HTTP_204_NO_CONTENT)

        else: 
            return Response({"status" : {"id" : ['id'+language.context[language.defaultLang]['missing']]}}, status=status.HTTP_400_BAD_REQUEST)             




