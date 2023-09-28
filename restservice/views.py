from django.shortcuts import render
from queue import Empty
from unicodedata import name
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
from NavyTrials import settings,language,error,common
import requests
import json


class VisaValidation(APIView):
	def post(self,request, pk = None):
		r = requests.post(url = settings.BIOMET_ENDPOINT+'QSysExt/services/demographic/details', json = request.data,headers={'Content-Type':'application/json'})
		if common.is_json(r.text):
			response = json.loads(r.text)
		else:
			response={'status':False,'message':language.context[language.defaultLang]['invalid_response']}
		response = {'status':error.context['success_code'] if r.status_code==200 and common.is_json(r.text) else error.context['error_code'],'response':response}
		return Response(response, status=status.HTTP_200_OK)

class VisaValidationTesting(APIView):
	def post(self,request):
		ra = requests.post(url = 'http://172.31.30.56:8000/api/auth/token', json = {'loginname':'etma','password':'Ditnavy@123'},headers={'Content-Type':'application/json'})
		authRes=json.loads(ra.text)
		Authorization='Bearer '+authRes['access']

		r = requests.post(url = 'http://172.31.30.56:8000/biomet/visa-validation', json = request.data,headers={'Content-Type':'application/json','Authorization':Authorization})
		if common.is_json(r.text):
			response = json.loads(r.text)
		else:
			response={'status':False,'message':language.context[language.defaultLang]['invalid_response']}
		response = {'status':error.context['success_code'] if r.status_code==200 and common.is_json(r.text) else error.context['error_code'],'response':response}
		return Response(response, status=status.HTTP_200_OK)

class VisaValidationInternal(APIView):
	def post(self,request):
		ra = requests.post(url = 'http://172.31.30.56:8000/api/auth/token', json = {'loginname':'etma','password':'Ditnavy@123'},headers={'Content-Type':'application/json'})
		authRes=json.loads(ra.text)
		Authorization='Bearer '+authRes['access']

		r = requests.post(url = 'http://172.31.30.56:8000/biomet/visa-validation', json = request.data,headers={'Content-Type':'application/json','Authorization':Authorization})
		if common.is_json(r.text):
			response = json.loads(r.text)
		else:
			response={'status':False,'message':language.context[language.defaultLang]['invalid_response']}
		response = {'status':error.context['success_code'] if r.status_code==200 and common.is_json(r.text) and 'statusCodeValue' not in response else error.context['error_code'],'response':response}
		return response

