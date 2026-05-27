from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao, verificar_token
from security import bcrypt_content, ALGORITHM, ACESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm


auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario, duracao_token = timedelta(minutes = ACESS_TOKEN_EXPIRE_MINUTES)):
    data_expericao = datetime.now(timezone.utc) + timedelta(minutes = ACESS_TOKEN_EXPIRE_MINUTES)
    dic_info = {"sub": str(id_usuario), "exp": data_expericao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM )
    return jwt_codificado



def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email). first()
    if not usuario:
        return False
    elif not bcrypt_content.verify(senha, usuario.senha ):
        return False
    return usuario

@auth_router.get('/')
async def home():
    '''
    Essa é a rota de autenticação para todos os usuários
    '''
    return {"mensagem": "você acessou a rota de autencação", "autenticado" : False}

@auth_router.post('/Criar conta')
async def criar_conta(usuario_schema: UsuarioSchema, session : Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email). first()
    if usuario:
        raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado")
    else:
        senha_criptografada = bcrypt_content.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin, )
        session.add(novo_usuario)
        session.commit()
        return{'mensagem ': "usuario cadastrado com sucesso"}

@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session= Depends(pegar_sessao) ):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="E-mail do usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        Refresh_token = criar_token(usuario.id)
        return {
            "access_token": access_token,
            "refresh_token": Refresh_token,
            "Token_type" : "Bearer"
        }


@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session= Depends(pegar_sessao) ):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="E-mail do usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token": access_token,
            "Token_type" : "Bearer"
        }        

@auth_router.get('/Reresh')
async def use_refresh_token(usuario:Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    return {
        "access_token": access_token,
        "token_type" : "bearer"
    }










