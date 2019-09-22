import re

from flask import request, url_for, redirect, g

from app import app
from app.models import user as users

def _opinar():
    """Permite ao usuário emitir uma opinião"""
    if request.method == "POST":
        tipo = request.form.get("tipo", None)
        texto = request.form.get("texto", None)
        foto = request.form.get("foto", None)
        post = request.form.get("post", None)
        user = g.user

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
            
            return redirect(rurl + str(r.id_post()))

    return ""