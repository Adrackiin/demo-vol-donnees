def file_is_present(file_name):
	try:
		fich = open(file_name, "rb")
		fich.close()
		return True
	except:
		return False
