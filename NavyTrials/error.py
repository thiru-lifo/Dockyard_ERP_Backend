context={
	"success_code":1,
	"error_code":2

}

def serializerError(saveserialize):
	errors=''
	for key, values in saveserialize.errors.items():
		error1 = [key+' - '+value[:] for value in values]
		errors+=error1[0]+' <br> '
	return errors