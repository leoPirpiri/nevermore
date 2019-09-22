import re
import os
import random
import cgi, cgitb

from flask import request, url_for, redirect, g

from app import app
from app.models import user as users


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
RND_STR = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else None

def allowed_file(filename):
    return get_extension(filename) in ALLOWED_EXTENSIONS

def _opinar():
    """Permite ao usuário emitir uma opinião"""
    if request.method == "POST":
        tipo = request.form.get("tipo", None)
        texto = request.form.get("texto", None)
        foto = request.files.get("foto", None)
        post = request.form.get("post", None)
        user = g.user
        
        if not foto is None and allowed_file(foto.filename):
            fext = ''.join(random.choices(RND_STR, k=30)) + '.' + get_extension(foto.filename)
            basedir = os.path.join(app.static_folder, app.config['IMAGES_USERS'])
            os.makedirs(basedir, exist_ok=True)
            foto.save(os.path.join(basedir, fext))
            foto = fext
        else:
            foto = None

        if texto is None or len(texto) > 500:
            return "Invalid length."

        if tipo == "POST" or tipo == "COMMENT":
            rurl = url_for("post")
            if rurl[-1] != '/':
                rurl += '/'
            
            from app.models.user import get_user
            _topicos  = set(i[1:] for i in re.findall('#\w+', texto))
            _marcados = [get_user(i[1:]) for i in set(re.findall('@\w+', texto))]
            _marcados = [i for i in _marcados if not i is None]
            
            if tipo == "POST":
                from app.models.post import criar_post
                r = criar_post(texto, foto, user, marcados=_marcados, topicos=_topicos)
            elif tipo == "COMMENT":
                if post is None or not post.isdigit():
                    return "Invalid operation."
                from app.models.comment import criar_comentario
                from app.models.post import Post
                r = criar_comentario(texto, foto, user, Post(int(post)), marcados=_marcados, topicos=_topicos)
            #terna o post que acabou de ser gravado no BD
            return (r.to_dict())
    return ""
