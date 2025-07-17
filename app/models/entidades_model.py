from pydantic import BaseModel
from datetime import date
from typing import List,Optional

class EntPubPriv(BaseModel):
    cod_ente: int
    cod_subente: int
    descrip_ente: str
    cuit_ente: Optional[int]
    suc_cta: Optional[int]
    prod_cta: Optional[int]
    num_cta: Optional[int]
    fec_inicio_act: Optional[date]
    fec_fin_act: Optional[date]
    clasif_ente: str
    modo_capt: str
    forma_acred: str
    conc_liquid: int
    porc_comi: float
    min_comi: float
    max_comi: float
    porc_rete: float
    form_arch_rend: str
    form_list_rend: str

class RuitConv(BaseModel):
    cod_convenio: Optional[int]
    fec_alta_convenio: date
    jur_const: Optional[int]
    pct_const: Optional[float]
    form_ruit: Optional[int]
    aut_const: Optional[int]
    jur_ruit: Optional[int]
    pct_jur: Optional[float]

class RuitJurisd(BaseModel):
    num_jurisd: int
    nom_jurisd: str
    fec_alta_jurisd: date
    imp_base_dist: float
    num_cbu: Optional[str]

