import json

WKHTML_PATH=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

def is_json(myjson):
	  try:
	    json.loads(myjson)
	  except ValueError as e:
	    return False
	  return True