from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema, ResponsePedidoSchema
from typing import List
from models import Pedido, Usuario, ItemPedido


order_router = APIRouter(prefix="/Pedidos", tags=["Pedidos"], dependencies=[Depends(verificar_token)])

@order_router.get('/')
async def pedidos():
    return {"mensagem": "voce acessou a rota de pedidos"}

@order_router.post('/pedido')
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario= pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {'mensagem': f"Pedido Criado com sucesso{novo_pedido.id}"}

@order_router.post('/pedido/cancelar/{id_pedido}')
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido). first()
    if not pedido:
        raise HTTPException(status_code= 400, detail='Pedido não encontrado')
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code= 401, detail='Você não possui autorização para cancelar esse pedido')
    pedido.status = "CANCELADO"
    session.commit()
    return{
        "mensagem": f'Pedido número : {pedido.id} cancelado com sucesso',
        "pedido" : pedido
    }

@order_router.get("/listar")
async def listar_pedidos(session: Session= Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code= 401, detail='Você não possui autorização para cancelar esse pedido')
    
    else:
        pedidos = session.query(Pedido).all()
        return{
            "pedidos": pedidos
        }

@order_router.post('/pedido/adicionar-item/{id_pedido}')
async def adicionar_item_pedido(id_pedido: int,
                                item_pedido_schema: ItemPedidoSchema,
                                session: Session =Depends(pegar_sessao),
                                usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id== id_pedido).first()
    if not pedido:
        raise HTTPException(status_code= 400, detail='Você não possui autorização para cancelar esse pedido')
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code= 401, detail='Você não possui autorização para cancelar esse pedido')
    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho, 
                             item_pedido_schema.preco_unitario, id_pedido)

    session.add(item_pedido)
    pedido.calcular_pedido()
    session.commit()
    return{
        "mensagem": "Item Criado com sucesso",
        "item_id" : item_pedido.id,
        "preco_pedido": pedido.preco
                }

@order_router.post('/pedido/remover-item/{id_item_pedido}')
async def adicionar_item_pedido(id_item_pedido: int,
                                session: Session =Depends(pegar_sessao),
                                usuario: Usuario = Depends(verificar_token)):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id== id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido).first()
    if not item_pedido:
        raise HTTPException(status_code= 400, detail='Este item não existe')
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code= 401, detail='Você não possui autorização para cancelar esse pedido')

    session.delete(item_pedido)
    pedido.calcular_pedido()
    session.commit()
    return{
        "mensagem": "Item removido com sucesso",
        "Quantidade_itens_peido": len(pedido.itens),
        "pedido" : pedido
                }
        

#finalizar o pedido
@order_router.post('/pedido/finalizar/{id_pedido}')
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido). first()
    if not pedido:
        raise HTTPException(status_code= 400, detail='Pedido não encontrado')
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code= 401, detail='Você não possui autorização para cancelar esse pedido')
    pedido.status = "FINALIZADO"
    session.commit()
    return{
        "mensagem": f'Pedido número : {pedido.id} finalizado com sucesso',
        "pedido" : pedido
    }

#visualizar o pedido
@order_router.get('/pedido/{id_pedido}')
async def visualizar_pedido(id_pedido: int, session: Session= Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido= session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code= 400, detail='Pedido não encontrado')
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code= 401, detail='Você não tem autorização para fazer esssa ação')
    return{
        "Quantidade_itens_pedido": len(pedido.itens),
        "pedido" : pedido
    }


#visualizar todos os pedidos de 1 usuário
@order_router.get('/listar/pedidos-usuario', response_model= List[ResponsePedidoSchema])
async def lista_pedidos(session: Session= Depends(pegar_sessao), usuario: Usuario= Depends(verificar_token)):
    pedidos = session.query(Pedido).filter(Pedido.usuario==usuario.id).all()
    return pedidos

    


