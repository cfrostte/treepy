"""..."""

from .core.Base import Base

class SurcoDetectadoParcela(Base):

    _tabla = 'surcos_detectados_parcelas'

    id_surcos_detectados = None
    id_parcelas = None

    def __init__(self, clave=None):
        Base.__init__(self, clave)

    @staticmethod
    def aleatorio():
        a = SurcoDetectadoParcela()
        return a

    @classmethod
    def sentencia(cls):
        s = """CREATE TABLE IF NOT EXISTS {} (
        clave INTEGER NOT NULL,
        id_surcos_detectados INTEGER NOT NULL,
        id_parcelas INTEGER NOT NULL,
        PRIMARY KEY(id_surcos_detectados, id_parcelas),
        FOREIGN KEY(id_surcos_detectados) REFERENCES surcos_detectados(clave),
        FOREIGN KEY(id_parcelas) REFERENCES parcelas(clave))"""
        return s.format(cls._tabla)
