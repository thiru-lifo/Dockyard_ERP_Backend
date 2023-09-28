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
from .models import  Modules, ModulesComponents,ModulesComponentsAttributes,AccessUserRoles,AccessModules,Privileges,RolesPermissions,Process, UserRoleDesignation
from .serializer import  ListModulesComponentserializer,Modulesserializer, ModulesComponentserializer,ListModulesComponentsAttributeserializer,ModulesComponentsAttributeserializer,AccessUserRoleserializer,AccessModuleserializer,ListAccessModuleserializer,Privilegesserializer,ListModulesserializer,AllModulesserializer,Permissionsserializer,Processserializer, UserRoleSerializer
from NavyTrials import language,error
from django.db.models import Count
from . import models

class Common:
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

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

            strings = ['name']
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

                list = Modules.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = ListModulesserializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)

        except Modules.DoesNotExist:

            return Response({"status" : error.context['error_code'],"message": "Modules"+language.context[language.defaultLang]['dataNotFound'] }, status = status.HTTP_200_OK)

        lists = Modules.objects.exclude(status='3')
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
        print(order_type is None)
        print(order_column)
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
        if not order_type and not order_column:
            lists = lists.order_by('sequence')

        serializer = ListModulesserializer(lists, many=True)
        return Response({"status": error.context['success_code'], "data": serializer.data}, status=status.HTTP_200_OK) 

class ModuleDetailViews(APIView):
        
    def get_object(self, pk):

        try:
            return Modules.objects.get(pk=pk)

        except Modules.DoesNotExist:
            raise Http404

    def post(self,request,pk=None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "Name"+language.context[language.defaultLang]['missing']  },status=status.HTTP_200_OK)
        elif 'process' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "process"+language.context[language.defaultLang]['missing']  },status=status.HTTP_200_OK)  
        elif 'type' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "type"+language.context[language.defaultLang]['missing']  },status=status.HTTP_200_OK)      
        else:    
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)                                       
                request.data['created_ip'] = created_ip 

                if not pk:
                    duplicate_name = Modules.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                                              
                    if duplicate_name:   
                        return Response({"status" :error.context['error_code'],"message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:

                        saveserialize = Modulesserializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" : error.context['success_code'],"message":"New modules"+language.context[language.defaultLang]['insert'] , "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" : error.context['error_code'], "message":error.serializerError(saveserialize)}, status=status.HTTP_200_OK)
            
                else: 

                    if request.data['status'] != 3:
                        
                        duplicate_name = Modules.objects.values('name').filter(name=request.data['name']).exclude(id=request.data['id'])
                        
                        if duplicate_name:   
                            return Response({"status" :error.context['error_code'],"message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    

                    list = self.get_object(pk)
                    saveserialize = Modulesserializer(list, data = request.data,partial=True)

                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'],"message": "modules"+language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" :error.context['error_code'],"message":error.serializerError(saveserialize)}, status=status.HTTP_200_OK) 
            else:        
                return Response({"status" : {"id" : ['id'+language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)             
        
class ModulesComponentsAttributeViews(APIView):

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

            strings = ['name']
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
                list = ModulesComponentsAttributes.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = ListModulesComponentsAttributeserializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
       
        except ModulesComponentsAttributes.DoesNotExist:
            return Response({"status" :error.context['error_code'],"message": "Modules component attributes"+language.context[language.defaultLang]['dataNotFound']}, status = status.HTTP_200_OK)

        lists = ModulesComponentsAttributes.objects.exclude(status='3')
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
       
        if not order_type and not order_column:
            lists = lists.order_by('sequence')
        serializer = ListModulesComponentsAttributeserializer(lists, many=True)
        return Response({"status":error.context['success_code'], "data": serializer.data}, status=status.HTTP_200_OK)

class ModulesComponentsAttributeDetail(APIView):

    def get_object(self,pk):

        try:
            return ModulesComponentsAttributes.objects.get(pk = pk)
        except ModulesComponentsAttributes.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "Name"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif 'module_component' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "module_component"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif 'type' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "type"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
       
        else:

            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)                                       
                request.data['created_ip'] = created_ip 
                
                if not pk: 
                    duplicate_name = ModulesComponentsAttributes.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                                                
                    if duplicate_name:   
                        return Response({"status" :error.context['error_code'],"message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
            
                        saveserialize = ModulesComponentsAttributeserializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" : error.context['success_code'],"message": "modules component attributes"+language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" : error.context['error_code'],"message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:

                    if request.data['status'] != 3:
                      
                        duplicate_name = ModulesComponentsAttributes.objects.values('name').filter(name=request.data['name']).exclude(id=request.data['id'])
                      
                        if duplicate_name:   
                            return Response({"status" :error.context['error_code'],"message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    

                    list = self.get_object(pk)
                    saveserialize = ModulesComponentsAttributeserializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" : error.context['success_code'],"message": "modules component attributes"+language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" : error.context['error_code'],"message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)
            else:        
                return Response({"status" : {"id" : ['id'+language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)            

class ModulesComponentsViews(APIView):

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

            strings = ['name']
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
                lists = ModulesComponents.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = ListModulesComponentserializer(lists)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)
            
        except ModulesComponents.DoesNotExist:
            return Response({"status" : error.context['error_code'],"message":"Module components"+language.context[language.defaultLang]['dataNotFound']}, status = status.HTTP_200_OK)

        lists = ModulesComponents.objects.exclude(status='3')

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
        
        if not order_type and not order_column:
            lists = lists.order_by('sequence')

        serializer = ListModulesComponentserializer(lists, many=True)
        return Response({"status": error.context['success_code'], "data": serializer.data}, status=status.HTTP_200_OK)

class ModulesComponentsDetail(APIView):

    def get_object(self,pk):

        try:
            return ModulesComponents.objects.get(pk = pk)
        except ModulesComponents.DoesNotExist:
            raise Http404


    def post(self,request, pk = None):
        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "Name"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif 'module' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "module"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)    
        elif 'type' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "type"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
          
        else: 
            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)                                       
                request.data['created_ip'] = created_ip 

                if not pk:

                    duplicate_name = ModulesComponents.objects.values('name').filter(name=request.data['name']).exclude(status=3)                           
                   
                    if duplicate_name:   
                        return Response({"status" :error.context['error_code'],"message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
            
                        saveserialize = ModulesComponentserializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" : "success","message": "module component"+language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'],"message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else:

                    if request.data['status'] != 3:
                       
                        duplicate_name = ModulesComponents.objects.values('name').filter(name=request.data['name']).exclude(id=request.data['id'])
                                         
                        if duplicate_name:   
                            return Response({"status" :error.context['error_code'],"message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    list = self.get_object(pk)
                    saveserialize = ModulesComponentserializer(list, data = request.data, partial= True)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" : error.context['success_code'],"message": "module component"+language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" : "error","message":error.serializerError(saveserialize)}, status = status.HTTP_200_OK)  
            else:        
                return Response({"status" : {"id" : ['id'+language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)                          

class AccessUserRolesView(APIView):

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
            process_id = request.GET.get('process_id')  
 
            if order_column is not None:                                      
                normal_values.pop('order_column')
            if order_type is not None: 
                normal_values.pop('order_type') 
            if limit_start is not None: 
                normal_values.pop('limit_start')
            if limit_end is not None: 
                normal_values.pop('limit_end')
            if process_id is not None: 
                normal_values.pop('process_id')
                 
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
                lists = AccessUserRoles.objects.filter(pk=pk).get()
                serializeobj = AccessUserRoleserializer(lists)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)

        except AccessUserRoles.DoesNotExist:
            return Response({"status" : error.context['error_code'],"message": "access user role"+language.context[language.defaultLang]['dataNotFound']}, status = status.HTTP_200_OK)

        lists = AccessUserRoles.objects.exclude(status=3)
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
        
        if process_id:
            lists=lists.filter(id__in=(models.ProcessRoleMapping.objects.values('user_role_id').filter(process_id=process_id)))
        
        serializer = AccessUserRoleserializer(lists, many=True)
        return Response({"status": error.context['success_code'], "data": serializer.data}, status=status.HTTP_200_OK)

class AccessUserRolesDetailsView(APIView):

    def get_object(self, pk):

        try:
            return AccessUserRoles.objects.get(pk=pk)
        except AccessUserRoles.DoesNotExist:
            raise Http404

    def post(self,request,pk=None):

        if 'from_ad' not in request.data and 'id' not in request.data:
                return Response({"status":error.context['error_code'],"message" : "from_ad"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif 'name' not in request.data and 'id' not in request.data:
                return Response({"status":error.context['error_code'],"message" : "Name"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif 'is_biometric' not in request.data and 'id' not in request.data:
            return Response({"status":error.context['error_code'],"message" : "is_biometric"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        else:
            if 'is_biometric' in request.data:
                request.data['is_biometric']=request.data['is_biometric'] if request.data['is_biometric'] else False
            if 'id' in request.data:
                pk = request.data['id']  
                created_ip = Common.get_client_ip(request)                                       
                request.data['created_ip'] = created_ip 

                if not pk:
                                    
                    saveserialize = AccessUserRoleserializer(data = request.data)

                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" : error.context['success_code'],"message": "access user role"+language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" : error.context['error_code'],"message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else: 
                    list = self.get_object(pk)
                    saveserialize = AccessUserRoleserializer(list,data = request.data,partial=True)

                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" :error.context['success_code'],"message": " access user role"+language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)

                    else:
                        return Response({"status" : error.context['error_code'],"message":error.serializerError(saveserialize)}, status=status.HTTP_200_OK) 
            else:        
                return Response({"status" : {"id" : ['id'+language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK) 

                    

class AccessModulesView(APIView):

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

            strings = ['name']
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
                list = AccessModules.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = ListAccessModuleserializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)

        except AccessModules.DoesNotExist:
            return Response({"status" : error.context['error_code'],"message": "Access modules"+language.context[language.defaultLang]['dataNotFound']}, status = status.HTTP_200_OK)

        lists = AccessModules.objects.exclude(status='3')

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
        if not order_type and not order_column:
            lists = lists.order_by('sequence')
        serializer = ListAccessModuleserializer(lists, many=True)
        return Response({"status": error.context['success_code'], "data": serializer.data}, status=status.HTTP_200_OK)

class AccessModulesDetailsView(APIView):

    def get_object(self, pk):

        try:
            return AccessModules.objects.get(pk=pk)
        except AccessModules.DoesNotExist:
            raise Http404

    def post(self,request,pk=None):
        
        if 'module' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "module"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif 'module_components' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "module components"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif 'module_components_attribute' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "module components_attribute"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif 'user_role' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "user role"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        
        else:

            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)                                       
                request.data['created_ip'] = created_ip 

                if not pk:
                    saveserialize = AccessModuleserializer(data = request.data)
                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" : error.context['success_code'],"message": "New access modules"+language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status" : error.context['error_code'],"message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else: 

                    list = self.get_object(pk)
                    saveserialize = AccessModuleserializer(list,data = request.data,partial=True)

                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" : error.context['success_code'],"message": "access module"+language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)

                    else:
                        return Response({"status" : error.context['error_code'],"message":error.serializerError(saveserialize)}, status=status.HTTP_200_OK) 
            else:        
                return Response({"status" : {"id" : ['id'+language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK) 

class PrivilegesView(APIView):

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
                list = Privileges.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = Privilegesserializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)

        except Privileges.DoesNotExist:
            return Response({"status" : error.context['error_code'],"message": "Privileges"+language.context[language.defaultLang]['dataNotFound']}, status = status.HTTP_200_OK)

        lists = Privileges.objects.exclude(status='3')
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
        
        if not order_type and not order_column:
            lists = lists.order_by('sequence')
        serializer = Privilegesserializer(lists, many=True)
        return Response({"status": error.context['success_code'], "data": serializer.data}, status=status.HTTP_200_OK)

class PrivilegesDetailsView(APIView):

    def get_object(self, pk):

        try:
            return Privileges.objects.get(pk=pk)
        except Privileges.DoesNotExist:
            raise Http404

    def post(self,request,pk=None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "Name"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "Code"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif 'description' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "description"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)        
        else:

            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)                                       
                request.data['created_ip'] = created_ip 

                if not pk:

                    duplicate_code = Privileges.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = Privileges.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'],"message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    if duplicate_name:   
                        return Response({"status" :error.context['error_code'],"message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:
                   
                        saveserialize = Privilegesserializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()
                            return Response({"status" :error.context['success_code'],"message": "privileges"+language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status" :error.context['error_code'],"message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else: 

                    if request.data['status'] != 3:

                        duplicate_code = Privileges.objects.values('code').filter(code=request.data['code']).exclude(id=request.data['id'])
                        duplicate_name = Privileges.objects.values('name').filter(name=request.data['name']).exclude(id=request.data['id'])
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'],"message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'],"message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    

                    list = self.get_object(pk)
                    saveserialize = Privilegesserializer(list,data = request.data,partial=True)

                    if saveserialize.is_valid():
                        saveserialize.save()
                        return Response({"status" : error.context['success_code'],"message": " privileges"+language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)

                    else:
                        return Response({"status" : error.context['error_code'],"message":error.serializerError(saveserialize)}, status=status.HTTP_200_OK) 
            else:        
                return Response({"status" : {"id" : ['id'+language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)            


class AllModuleViews(APIView):

    def get(self, request, pk = None):
        filter_values = dict(request.GET.items())
        searchFilter={}
        if 'process_id' in filter_values:
            searchFilter['process_id']=filter_values['process_id']

        lists = Modules.objects.filter(**searchFilter).exclude(status='3').order_by('sequence')

        serializer = AllModulesserializer(lists, many=True)
        return Response({"status":error.context['success_code'], "data": serializer.data}, status=status.HTTP_200_OK) 

class ProcessViews(APIView):

    def get(self, request, pk = None):
        filter_values = dict(request.GET.items())
        searchFilter={}

        lists = Process.objects.filter(**searchFilter).order_by('sequence')

        serializer = Processserializer(lists, many=True)
        return Response({"status":error.context['success_code'], "data": serializer.data}, status=status.HTTP_200_OK) 

# Create your views here.

class PermissionsView(APIView):

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
                list = RolesPermissions.objects.filter(pk=pk).get()
                serializeobj = Privilegesserializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)

        except RolesPermissions.DoesNotExist:
            return Response({"status" : error.context['error_code'],"message": "Permissions"+language.context[language.defaultLang]['dataNotFound']}, status = status.HTTP_200_OK)

        lists = RolesPermissions.objects
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
        serializer = Permissionsserializer(lists, many=True)
        return Response({"status": error.context['success_code'], "data": serializer.data}, status=status.HTTP_200_OK)

class PermissionsDetailsView(APIView):

    def get_object(self, pk):

        try:
            return RolesPermissions.objects.get(pk=pk)
        except Privileges.DoesNotExist:
            raise Http404

    def post(self,request,pk=None):
        if 'id' in request.data:
            pk = request.data['id']
            
            if not pk:
                try:
                    models.RolesPermissions.objects.filter(process_id=request.data['process'],user_role_id=request.data['user_role']).delete()
                except:
                    deleted='no matching query found'
                saveserialize = Permissionsserializer(data = request.data)
                if saveserialize.is_valid():
                    saveserialize.save()
                    return Response({"status" : error.context['success_code'],"message": "Privileges"+language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                else:
                    return Response({"status" :error.context['error_code'],"message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

            else:
                print(request.data['process'],request.data['user_role'])
                try: 
                    models.RolesPermissions.objects.filter(process_id=request.data['process'],user_role_id=request.data['user_role']).delete()
                except:
                    deleted='no matching query found'
                # list = self.get_object(pk)
                saveserialize = Permissionsserializer(data = request.data)

                if saveserialize.is_valid():
                    saveserialize.save()
                    return Response({"status" : error.context['success_code'],"message": " Privileges"+language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)

                else:
                    return Response({"status" :error.context['error_code'],"message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK) 
        else:        
            return Response({"status" : {"id" : ['id'+language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)            


# User Role

class UserRoleView(APIView):

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
                list = AccessUserRoles.objects.filter(pk=pk).exclude(status='3').get()
                serializeobj = UserRoleSerializer(list)
                return Response({"status": error.context['success_code'], "data": serializeobj.data}, status=status.HTTP_200_OK)

        except AccessUserRoles.DoesNotExist:
            return Response({"status" : error.context['error_code'],"message": "AccessUserRoles"+language.context[language.defaultLang]['dataNotFound']}, status = status.HTTP_200_OK)

        lists = AccessUserRoles.objects.exclude(status='3')
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
        
        if not order_type and not order_column:
            lists = lists.order_by('name')
        serializer = UserRoleSerializer(lists, many=True)
        return Response({"status": error.context['success_code'], "data": serializer.data}, status=status.HTTP_200_OK)

class UserRoleDetailsView(APIView):

    def get_object(self, pk):

        try:
            return AccessUserRoles.objects.get(pk=pk)
        except AccessUserRoles.DoesNotExist:
            raise Http404

    def post(self,request,pk=None):

        if 'name' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "Name"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        elif 'code' not in request.data and request.data['status'] != 3:
            return Response({"status":error.context['error_code'],"message" : "Code"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)
        #elif 'description' not in request.data and request.data['status'] != 3:
            #return Response({"status":error.context['error_code'],"message" : "description"+language.context[language.defaultLang]['missing'] },status=status.HTTP_200_OK)        
        else:

            if 'id' in request.data:
                pk = request.data['id']
                created_ip = Common.get_client_ip(request)                                       
                #request.data['created_ip'] = created_ip 

                if not pk:

                    duplicate_code = AccessUserRoles.objects.values('code').filter(code=request.data['code']).exclude(status=3)
                    duplicate_name = AccessUserRoles.objects.values('name').filter(name=request.data['name']).exclude(status=3)
                            
                    if duplicate_code:            
                        return Response({"status" :error.context['error_code'],"message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                    
                    if duplicate_name:   
                        return Response({"status" :error.context['error_code'],"message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    
                    else:

                        #print(type(request.data['designations']),"Type of ######")
                   
                        saveserialize = AccessUserRoleserializer(data = request.data)
                        if saveserialize.is_valid():
                            saveserialize.save()


                            #designations = request.data['data_access']
                            running_id = saveserialize.data['id']
                            created_ip = created_ip
                            
                            # for access in (request.data['data_access']):
                            #     models.UserRoleDesignation.objects.create(
                            #         user_role_id = running_id,
                            #         designation = access['designation'],
                            #         status = '2',
                            #         created_ip = created_ip
                            #     )



                            for designation in (request.data['designations']):
                                models.UserRoleDesignation.objects.create(
                                    user_role_id = running_id,
                                    designation = designation,
                                    status = '2',
                                    created_ip = created_ip
                                )


                            return Response({"status" :error.context['success_code'],"message": "UserRole"+language.context[language.defaultLang]['insert'], "data":saveserialize.data}, status=status.HTTP_200_OK)
                            running_id = saveserialize.data['id']
                        else:
                            return Response({"status" :error.context['error_code'],"message": error.serializerError(saveserialize)}, status=status.HTTP_200_OK)

                else: 

                    if request.data['status'] != 3:

                        duplicate_code = UserRole.objects.values('code').filter(code=request.data['code']).exclude(id=request.data['id'])
                        duplicate_name = UserRole.objects.values('name').filter(name=request.data['name']).exclude(id=request.data['id'])
                        if duplicate_code:            
                            return Response({"status" :error.context['error_code'],"message":language.context[language.defaultLang]['exit code'] },status=status.HTTP_200_OK)                    
                        elif duplicate_name:   
                            return Response({"status" :error.context['error_code'],"message":language.context[language.defaultLang]['exit name'] },status=status.HTTP_200_OK)                    
                    

                    list = self.get_object(pk)
                    saveserialize = AccessUserRoleserializer(list,data = request.data,partial=True)

                    if saveserialize.is_valid():
                        saveserialize.save()

                        UserRoleDesignation.objects.filter(user_role_id=request.data['id']).delete()

                        # for access in (request.data['data_access']):
                        #     models.UserRoleDesignation.objects.create(
                        #         user_role_id = request.data['id'],
                        #         designation = access['designation'],
                        #         status = '2',
                        #         created_ip = created_ip
                        #     )

                        for designation in (request.data['designations']):
                            models.UserRoleDesignation.objects.create(
                                user_role_id = request.data['id'],
                                designation = designation,
                                status = '2',
                                created_ip = created_ip
                            )

                        return Response({"status" : error.context['success_code'],"message": " UserRole"+language.context[language.defaultLang]['update'], "data":saveserialize.data}, status=status.HTTP_200_OK)

                    else:
                        return Response({"status" : error.context['error_code'],"message":error.serializerError(saveserialize)}, status=status.HTTP_200_OK) 
            else:        
                return Response({"status" : {"id" : ['id'+language.context[language.defaultLang]['missing']]}}, status=status.HTTP_200_OK)            

