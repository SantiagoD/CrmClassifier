import csv
import datetime
import os
import aes_encription as aenc 

key = '0123456789abcdef'
	

def registrar_classificacao(texto, resultado):


	#definir mes atual
	now = datetime.datetime.now()

	logname = 'log_' + str(now.month) + '_' + str(now.year)
	enc_mail = aenc.encrypt_text(key, texto + str(resultado))
	#verifica arquivo
	if os.path.isfile(logname + '.csv'):
		with open(logname + '.csv', 'a', newline='') as csvfile:
		    logwriter = csv.writer(csvfile, delimiter=' ',
		                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
		    #logwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
		    logwriter.writerow([str(now), texto, resultado, enc_mail])
		
	else:
		with open(logname + '.csv', 'w', newline='') as csvfile:
		    logwriter = csv.writer(csvfile, delimiter=' ',
		                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
		    logwriter.writerow(['data', 'conteudo', 'resultado', 'hash'])
		    logwriter.writerow([str(now), texto, resultado, enc_mail])
	return True

#password = "exc_CRM_12345678"


# import hashlib

# password = 'EXC_crm'
# key = hashlib.sha256(password).digest()

# mode = AES.MODE_CBC
# encryptor = AES.new(key, mode, IV=IV)

now = datetime.datetime.now()
lastmonth = now.month - 1
lastmonthyear = now.year

if lastmonth == 0:
	lastmonth = 12
	lastmonthyear = lastmonthyear - 1

logname = 'log_' + str(lastmonth) + '_' + str(lastmonthyear)


in_filename = logname +'.csv'
out_filename = logname +'_enc.csv'

# with open(in_filename, 'rb') as in_file, open(out_filename, 'wb') as out_file:
aenc.encrypt_file(key, in_filename, out_filename)

in_filename = out_filename 
out_filename = logname +'_dec.csv'

# with open(in_filename, 'rb') as in_file, open(out_filename, 'wb') as out_file:
aenc.decrypt_file(key, in_filename, out_filename)

# with open(in_filename, 'rb') as in_file, open(out_filename, 'wb') as out_file:
#     clen.encrypt(in_file, out_file, password)

# in_filename = out_filename 
# out_filename = 'log_01_2017_dec.csv'
# with open(in_filename, 'rb') as in_file, open(out_filename, 'wb') as out_file:
#     clen.decrypt(in_file, out_file, password)