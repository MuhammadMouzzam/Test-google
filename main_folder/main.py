import re
from fastapi import FastAPI
from fastapi.requests import Request
from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.middleware.sessions import SessionMiddleware
from .config import settings


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key='this_is_just_a_random_key')

auth = OAuth()
auth.register(
    name = 'google',
    server_metadata_url = 'https://accounts.google.com/.well-known/openid-configuration',
    client_id = settings.client_id,
    client_secret = settings.client_secret,
    client_kwargs = {
        'scope' : 'email openid profile',
        'redirect_url' : 'http://127.0.0.1:8080/auth'
    }
)

@app.get('/')
def main_page():
    return 'Hello World'

@app.get('/login')
async def login(request : Request):
    url = request.url_for('autho')
    return await auth.google.authorize_redirect(request, url)
    
@app.get('/auth')
async def autho(request : Request):
    try:
        token = await auth.google.authorize_access_token(request)
    except OAuthError as e:
        return "Authentication Failed"
    user = token.get('userinfo')
    if user:
        request.session['user'] = user
    return user