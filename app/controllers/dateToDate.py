class Data:
    def __init__(self, dia, hora):
        self.dias = dia
        self.horas = hora

def formatDate(data):
    data = data.split(' ')
    dia = data[0].split('-')
    dia = '-'.join(dia.reverse())
    hora= data[1][0:5]
    return Data(dia, hora)