from pydantic import BaseModel
from datetime import date
from typing import List,Optional

class Lote650(BaseModel):
    cod_ordenante: str
    id_operacion: int
    fec_pago: date
    imp_cesion: float
    cant_trans: int

class DetLote650(BaseModel):
    cod_ordenante: str
    id_operacion: int
    fec_pago: date
    imp_cesion: float
    cant_trans: int
    num_orden: int
    imp_orden: float
    num_cbu_destino: str

class Prod650Vig(BaseModel):
    cod_ordenante: Optional[str]
    fec_alta_contrato: date
    cod_modalidad_producto: Optional[int]
    desc_modalidad_producto: Optional[str]
    id_d_contrato_debito: Optional[int]
    suc_cta_debito: Optional[int]
    prod_cta_debito: Optional[int]
    num_cta_debito: Optional[int]
    fec_ult_lote: Optional[date]

class OrdenanteDesc(BaseModel):
    desc_ordenante: str
