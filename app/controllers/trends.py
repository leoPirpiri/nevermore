def get_assuntos(assuntos):
    momentos = []
    momentos.append({'nome': 'UlyssesReitor', 'quan': 1206})
    momentos.append({'nome': 'CãoBemArticulado', 'quan': 756})
    momentos.append({'nome': 'AllanDiretor', 'quan': 588})
    momentos.append({'nome': 'tudoTranquilo', 'quan': 44})
    for assunto in assuntos:
        momentos.append(assunto)
    return momentos