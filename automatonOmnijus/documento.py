
from attr import has
from automatonOmnijus.rotas import * 
from automatonOmnijus.requisicao import faz_requisicao
from automatonOmnijus.rotas import VISUALIZAR_DOCUMENTO
from requests import get
class Documento:

     def __init__(self,senha:str,ambiente:str,processo:str,nome:str=None,hash:str=None,offline:bool=False) -> None:
        self.num_processo = processo
        self.nome = nome
        self.hash = hash 
        self._offline = offline 
        
        self._headers = {
        'senha':senha,
        'ambiente':ambiente,
        'processo':str(processo),
        'documento':nome,
        'hash':hash,
        'baixar':'true'
       }
    
    
     def baixar_binario_do_documento(self)->bytes:
         """ Baixa binário do documento
         Returns:
             bytes: o binário do documento 
         """
         req ={
            'url':f'{URL}{VISUALIZAR_DOCUMENTO}',
            'headers':self._headers
         }
         doc = get(**req)
         return doc.content
    
     def baixar_documento(self,path:str=None):
         """ Baixa o documento do processo
         Args:
             path (str, optional): Onde salvar o documento. Defaults to None.
         """
         if path is None:
            path = self.nome
         binario = self.baixar_binario_do_documento()
         with open(path,'wb') as f:
            f.write(binario)
            f.close()
            
     def gerar_url(self)->str:
         """_cria a url do Documento
         Returns:
             str: a url do documento 
         """
         query_string = ''
         copia_headers = self._headers.copy()
         copia_headers['baixar'] = 'false'
         copia_headers.pop('senha')
         for x in copia_headers:
             query_string += f'{x}={copia_headers[x]}&'
         return f'{URL}{VISUALIZAR_DOCUMENTO}?{query_string}'


     def fazer_upload_de_documento(self,path:str):
        with open(path,'rb') as f:
            binario = f.read()
            faz_requisicao(headers=self._headers,rota=ADICIONAR_DOCUMENTO_DO_PROCESSO,body=binario)


     def __repr__(self):
        return f"""Documento: {self.nome}
Hash: {self.hash}
Offline: {self._offline}
Query string: {self.gerar_url()}"""

