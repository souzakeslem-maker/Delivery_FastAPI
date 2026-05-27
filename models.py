from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
# from sqlalchemy_utils import ChoiceType


#cria a conexão do seu banco
db = create_engine("sqlite:///banco.db")

#cria a base do banco de dados
base = declarative_base()

#criar uas classe/tabelas do banco
class Usuario(base):
    __tablename__ = 'Usuarios'

    id = Column('id', Integer, primary_key= True, autoincrement=True)
    nome = Column('nome', String)
    email = Column('email', String, nullable= False)
    senha = Column('senha', String)
    ativo = Column('ativo', Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin= False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


# Pedido
class Pedido(base):
    __tablename__ = "pedidos"


    id = Column('id', Integer, primary_key= True, autoincrement=True)
    status = Column("status", String)
    usuario = Column("usuario", ForeignKey('Usuarios.id')) #para ligar com a tabela de usuários
    preco = Column('preco', Float)
    itens = relationship("ItemPedido", cascade='all, delete')

    def __init__(self, usuario, status= "Pendente", preco=0,):
        self.usuario = usuario
        self.preco = preco
        self.status = status

    def calcular_pedido(self):
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)
        


#Itens Pedido
class ItemPedido(base):
    __tablename__ = 'itens_pedido'

    id = Column('id', Integer, primary_key= True, autoincrement=True)
    quantidade = Column('quantidade', Integer)
    sabor = Column('sabor', String)
    tamanho = Column('tamanho', String)
    preco_unitario = Column('preco_unitario', Float)
    pedido = Column('pedido', ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor,tamanho,  preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido








