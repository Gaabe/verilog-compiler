import sys
sys.path.insert(0, 'lib')

import syntax_verifier
import os.path

file_path = sys.argv[1]

if os.path.isfile(file_path):
	file_object = open(file_path,'r')
	syntax_verifier.init(file_object)
else:
	print('Arquivo inválido, por favor verifique se o caminho foi informado corretamente.')