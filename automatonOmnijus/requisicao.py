from automatonOmnijus.rotas import *
from json import JSONDecodeError,loads
from requests import get



def faz_requisicao(headers:dict,rota,body=None)->str or dict or list:
    
    if rota not in ROTAS_VALIDAS:
        raise Exception(f'a rota "{rota}" não existe')
        
    URL = 'https://75s7k5xf4ebqh2sofe676zh7gm0vedtt.lambda-url.us-east-1.on.aws'
    req ={
        'url':f'{URL}{rota}',
        'headers':headers
    }
    if body.__class__ == dict:
        req['json']= body

    http = get(**req)

    if http.status_code != 200:
        raise Exception(http.text)
    
    else:
        try:
            return loads(http.text)
        except JSONDecodeError:
            return http.text
    
