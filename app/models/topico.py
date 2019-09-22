try:
    from app.models.base import Base, Stub
    from app.models import db_wrapper
except:
    from . import Base, Stub
    from . import db_wrapper

def __criar_topico(nome_topico):
    if db_wrapper.get_topico_pk(nome_topico) is None:
        db_wrapper.inserir_topico({'nome_topico': nome_topico})