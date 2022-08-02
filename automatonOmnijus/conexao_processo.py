from copy import deepcopy
from json import dumps
from automatonOmnijus.documento import Documento
from automatonOmnijus.requisicao import faz_requisicao
from typing import List
from automatonOmnijus.rotas import *



class ConexaoProcesso:

    def __init__(self,senha:str,ambiente:str,processo:str,offline:bool=False,carregar:bool=False) -> None:
        self.num_processo = processo
        self.dados_do_processo = {}
        self.estado = {}
        self.acoes = []
        self.documentos:List[Documento] =[]
        self._senha = senha
        self._ambiente = ambiente
        self._carregado = False 
        self._offline = offline 
        self._headers = {
        'senha':senha,
        'ambiente':ambiente,
        'processo':str(processo)
       }
    
        if carregar:
            self.carregar_processo()
            self._carregado = True



    def criar_processo(self):
        """Cria um novo processo novo
        Args:
            dados_do_processo (dict): Dicionário com os dados do processo
            estado (dict): Estado do processo
            acoes (List[dict]): Lista de ações do processo
        """
        if self._offline:return 
        dados = {
            'processo':self.dados_do_processo,
            'estado':self.estado,
            'acoes':self.acoes
        }
        faz_requisicao(headers=self._headers,rota=CRIAR_PROCESSO,body=dados)
        self._carregado = True 

    

    def excluir_processo(self):
        """Exclui o processo""" 
        if self._offline:return 
        faz_requisicao(headers=self._headers,rota=EXCLUIR_PROCESSO)
        self._carregado = False
    
    def carregar_processo(self):
        """Carrega o processo
        Returns:
            dict: Dicionário com o processo
        """
        if self._offline:return 
        carregamento = faz_requisicao(headers=self._headers,rota=DADOS_DO_PROCESSO)
        self.dados_do_processo = carregamento['processo']
        self.estado = carregamento['estado']
        self.acoes = carregamento['acoes']
        for doc in carregamento['documentos']:
            self.documentos.append(Documento(
                senha=self._senha,
                ambiente=self._ambiente,
                nome=doc['nome'],
                hash=doc['hash'],
                processo=self.num_processo,
                offline=self._offline
            ))
        self._carregado = True
        return self 


    def verifica_se_esta_carregado(self):
        """Verifica se o processo está carregado"""
        if not self._carregado:
            raise Exception('O processo não foi carregado')

    def salvar_processo_localmente(self):
        """Salva os dados do processo"""
        if self._offline:return 
        self.verifica_se_esta_carregado()    
        dados = {
            'processo':self.dados_do_processo,
            'estado':self.estado,
            'acoes':self.acoes
        }
        
        faz_requisicao(headers=self._headers,rota=MODIFICAR_PROCESSO,body=dados)


    def documento(self,nome:str=None,hash:str=None) -> Documento:
        """Retorna um documento do processo
        Args:
            nome (str): Nome do documento
            hash (str): Hash do documento
        Returns:
            Documento: Documento do processo
        """
        for doc in self.documentos:
            if not nome:
                if doc.hash == hash:
                    return doc
            elif not hash:
                if doc.nome == nome:
                    return doc
            elif doc and hash:
                if doc.nome == nome and doc.hash == hash:
                    return doc
            else:
                raise Exception('Nome ou hash não fornecidos')
        
        self.documentos.append(
            Documento(senha=self._senha,
                      ambiente=self._ambiente,
                      nome=nome,
                      hash=hash,
                      processo=self.num_processo,
                      offline=self._offline
            )
        )




    def __repr__(self) -> str:

        #ident the is of documents in tab 4

        text = '\n' + '=' *100 + f"""\nProcesso: {self.num_processo}
Carregado: {self._carregado}
Offline: {self._offline}
Estado: {self.estado}
Dados do processo: {dumps(self.dados_do_processo,indent=4)}
Acoes: {dumps(self.acoes,indent=4)}
"""
        text+='Documentos:'
        for doc in self.documentos:
            text+='\n\t' + '-'* 100
            text += '\n\t' + str(doc).replace('\n','\n\t') 

        return text