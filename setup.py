from setuptools import setup

setup(
    name='automatonOmnijus',
    packages=['automatonOmnijus'],
    description='wraper de conexão com a Central Omnijus',
    version='0.1',
    url='https://github.com/Mateusominjus/AutomatonOmnijus.git',
    author='Mateus',
    author_email='mateus.queiroz@omnijus.com.br',
    keywords=['omnius','lawTec'],
    install_requires=['requests'],
)

#para instalar  pip install --upgrade git+https://github.com/Mateusominjus/AutomatonOmnijus.git