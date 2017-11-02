import re

def devolve_requisito(tipo, texto):
	if tipo == 'cpf':
		expressao = '([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})'
	resultado = re.findall(expressao, texto)
	return resultado
