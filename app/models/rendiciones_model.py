from pydantic import BaseModel
from typing import Optional
from datetime import date,datetime

class RendicionEnte(BaseModel):
    cod_ente: int
    cod_subente: int
    fecha_pago: Optional[date]
    fecha_rendicion: Optional[date]
    cod_banco: Optional[int]
    cod_ubicacion: Optional[int]
    num_terminal: Optional[int]
    num_comprob: Optional[int]
    imp_cobrado: Optional[float]
    imp_retencion: Optional[float]
    imp_comision: Optional[float]
    cod_barra: Optional[str]
    banco_cheque: Optional[int]
    num_cheque: Optional[int]
    estado_rendicion: Optional[str]
    forma_pago: Optional[str]

class MovCtas(BaseModel):
    fec_evento: date
    hora_evento: str
    fec_valor: date
    imp_mvto: float
    imp_saldo: float
    desc_mvto: Optional[str]
