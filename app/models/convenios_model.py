from pydantic import BaseModel
from datetime import date
from typing import List,Optional

class ConveniosEntes2(BaseModel):
    cod_ente: Optional[int]
    canal_cobranza: int
    nombre_cabecera: str
    tipo_ente: int
    condicion_registro_id_ente: Optional[int]
    fec_alta_ente: Optional[date]
    fecha_baja: Optional[date]
    id_diseño: int
    nombre_diseño: str
    longitud_diseño: int
    tipo_importe: Optional[int]
    fec_alta_diseño: Optional[date]
    contienedv: Optional[int]
    desactivarcontroldv: Optional[int]
    condicion_registro_id_diseño: Optional[int]


    