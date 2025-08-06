from http.client import HTTPException
from fastapi import APIRouter, Query
from app.database.teradata_connection import get_teradata_connection
from app.models.rendiciones_model import RendicionEnte,MovCtas,ClienteDesc
from typing import List, Optional
import app.utils.helpers as helpers

router = APIRouter()

@router.get("/Rendiciones/Entes", response_model=List[RendicionEnte])
def obtener_rend_entes(
    cod_convenio: Optional[int] = Query(None),
    cod_sub_convenio: Optional[int] = Query(None),
    cod_ubicacion: Optional[int] = Query(None),
    fec_ini_rend: str = Query(...),
    fec_fin_rend: str = Query(...)    
):
    try:
        conn = get_teradata_connection()
        cursor = conn.cursor()
        
        if cod_ubicacion and cod_ubicacion > 0:
            if cod_convenio and cod_convenio > 0:
                sql = """
                    SELECT D.cod_Convenio_Entidad as cod_ente, D.cod_sub_convenio_entidad as cod_subente, 
                    D.fec_evento as fecha_pago, D.fec_rendicion_entidad as fecha_rendicion, D.cod_banco,
                    D.cod_ubicacion, D.num_terminal, D.num_comprobante_entidad as num_comprob,
                    D.mto_recaudacion_entidad as imp_cobrado, D.mto_retencion_entidad as imp_retencion,
                    D.mto_comision_entidad as imp_comision, D.cod_barra_entidad as cod_barra,
                    D.cod_banco_cheque_entidad as banco_cheque, D.num_cheque_entidad as num_cheque,
                    CASE
                        WHEN D.cod_estado_rendicion_entidad = 1 THEN 'RENDIDO'
                        ELSE 'PENDIENTE' END AS estado_rendicion,
                    CASE
                        WHEN D.cod_situacion_cheque_entidad = 0 THEN 'EFECTIVO'
                        WHEN D.cod_situacion_cheque_entidad = 1 THEN 'CHEQ PRES'
                        WHEN D.cod_situacion_cheque_entidad = 2 THEN 'CHEQ CONF'
                        WHEN D.cod_situacion_cheque_entidad = 3 THEN 'CHEQ RECH'
                    END AS forma_pago
                    FROM P_SEM_VIEWS.f_recaudaciones_entidades D
                    WHERE D.cod_Convenio_Entidad = ?
                    AND D.cod_sub_convenio_entidad = ?
                    AND D.cod_ubicacion = ?
                    AND D.fec_rendicion_entidad BETWEEN ? AND ?
                    AND D.cod_convenio_entidad NOT IN (200)
                    ORDER BY D.fec_rendicion_entidad, D.cod_convenio_entidad, D.cod_sub_convenio_entidad, D.fec_rendicion_Entidad, 
                    D.cod_ubicacion
                """
                cursor.execute(sql, (cod_convenio, cod_sub_convenio, cod_ubicacion, fec_ini_rend, fec_fin_rend))
            else:
                sql = """
                    SELECT D.cod_Convenio_Entidad as cod_ente, D.cod_sub_convenio_entidad as cod_subente, 
                    D.fec_evento as fecha_pago, D.fec_rendicion_entidad as fecha_rendicion, D.cod_banco,
                    D.cod_ubicacion, D.num_terminal, D.num_comprobante_entidad as num_comprob,
                    D.mto_recaudacion_entidad as imp_cobrado, D.mto_retencion_entidad as imp_retencion,
                    D.mto_comision_entidad as imp_comision, D.cod_barra_entidad as cod_barra,
                    D.cod_banco_cheque_entidad as banco_cheque, D.num_cheque_entidad as num_cheque,
                    CASE
                        WHEN D.cod_estado_rendicion_entidad = 1 THEN 'RENDIDO'
                        ELSE 'PENDIENTE' END AS estado_rendicion,
                    CASE
                        WHEN D.cod_situacion_cheque_entidad = 0 THEN 'EFECTIVO'
                        WHEN D.cod_situacion_cheque_entidad = 1 THEN 'CHEQ PRES'
                        WHEN D.cod_situacion_cheque_entidad = 2 THEN 'CHEQ CONF'
                        WHEN D.cod_situacion_cheque_entidad = 3 THEN 'CHEQ RECH'
                    END AS forma_pago
                    FROM P_SEM_VIEWS.f_recaudaciones_entidades D
                    WHERE D.cod_ubicacion = ?
                    AND D.fec_rendicion_entidad BETWEEN ? AND ?
                    AND D.cod_convenio_entidad NOT IN (200)
                    ORDER BY D.fec_rendicion_entidad, D.cod_convenio_entidad, D.cod_sub_convenio_entidad, D.fec_rendicion_Entidad, 
                    D.cod_ubicacion
                """
                cursor.execute(sql, (cod_ubicacion, fec_ini_rend, fec_fin_rend))

        else:    
            sql = """
                SELECT D.cod_Convenio_Entidad as cod_ente, D.cod_sub_convenio_entidad as cod_subente, 
                D.fec_evento as fecha_pago, D.fec_rendicion_entidad as fecha_rendicion, D.cod_banco,
                D.cod_ubicacion, D.num_terminal, D.num_comprobante_entidad as num_comprob,
                D.mto_recaudacion_entidad as imp_cobrado, D.mto_retencion_entidad as imp_retencion,
                D.mto_comision_entidad as imp_comision, D.cod_barra_entidad as cod_barra,
                D.cod_banco_cheque_entidad as banco_cheque, D.num_cheque_entidad as num_cheque,
                CASE
                    WHEN D.cod_estado_rendicion_entidad = 1 THEN 'RENDIDO'
                    ELSE 'PENDIENTE' END AS estado_rendicion,
                CASE
                    WHEN D.cod_situacion_cheque_entidad = 0 THEN 'EFECTIVO'
                    WHEN D.cod_situacion_cheque_entidad = 1 THEN 'CHEQ PRES'
                    WHEN D.cod_situacion_cheque_entidad = 2 THEN 'CHEQ CONF'
                    WHEN D.cod_situacion_cheque_entidad = 3 THEN 'CHEQ RECH'
                END AS forma_pago
                FROM P_SEM_VIEWS.f_recaudaciones_entidades D
                WHERE D.cod_Convenio_Entidad = ?
                AND D.cod_sub_convenio_entidad = ?
                AND D.fec_rendicion_entidad BETWEEN ? AND ?
                AND D.cod_convenio_entidad NOT IN (200)
                ORDER BY D.fec_rendicion_entidad, D.cod_convenio_entidad, D.cod_sub_convenio_entidad, D.fec_rendicion_Entidad, 
                D.cod_ubicacion
            """
            cursor.execute(sql, (cod_convenio, cod_sub_convenio, fec_ini_rend, fec_fin_rend))
        
        results = helpers.query_to_dict_list(cursor)
        return results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en /Rendiciones/Entes: {str(e)}")        
    finally:
        cursor.close()
        conn.close()

@router.get("/Rendiciones/MovCtas", response_model=List[MovCtas])
def obtener_movimientos(
    cod_ubicacion: int = Query(None),
    cod_producto: int = Query(None),
    num_cuenta: int = Query(None),
    fec_ini_mvto: str = Query(...),
    fec_fin_mvto: str = Query(...)    
):
    try:
        conn = get_teradata_connection()
        cursor = conn.cursor()
        sql = """
            SELECT B.fec_evento,Cast( B.hora_evento AS CHAR(8)) AS hora_evento,B.fec_valor, 
            B.Mto_Evento AS imp_mvto, B.mto_saldo AS imp_saldo,d.DESC_movimiento_TRX AS desc_mvto
            FROM P_SEM_VIEWS.d_contratos_actual c
            INNER JOIN P_SEM_VIEWS.f_cuentas_depositos b
                ON c.id_d_contrato = b.id_d_contrato
            INNER JOIN P_SEM_VIEWS.d_movimientos_trx d
                ON b.cod_movimiento_trx = d.cod_movimiento_trx
            WHERE c.cod_ubicacion = ?
                AND c.id_d_producto = ?
                AND c.num_cuenta = ?
                AND b.fec_evento BETWEEN ? AND ?
            ORDER BY fec_evento,hora_evento
        """
        cursor.execute(sql, (cod_ubicacion, cod_producto, num_cuenta, fec_ini_mvto, fec_fin_mvto))
        results = helpers.query_to_dict_list(cursor)
        return results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en /Rendiciones/MovCtas: {str(e)}")        
    finally:
        cursor.close()
        conn.close()

@router.get("/Rendiciones/ClienteDesc", response_model=ClienteDesc)
def obtener_descrip_cliente(
    cod_ubicacion: int = Query(None),
    cod_producto: int = Query(None),
    num_cuenta: int = Query(None)
):
    try:
        conn = get_teradata_connection()
        cursor = conn.cursor()

        sql = """
            SELECT D.NOM_CLIENTE FROM P_SEM_VIEWS.D_CONTRATOS_ACTUAL C
            INNER JOIN P_SEM_VIEWS.D_CLIENTES_ACTUAL D
	            ON C.ID_D_CLIENTE = D.ID_D_CLIENTE
            WHERE COD_UBICACION = ?
            AND ID_D_PRODUCTO = ?
            AND NUM_CUENTA = ?
        """
        cursor.execute(sql, (cod_ubicacion, cod_producto, num_cuenta))
        result = cursor.fetchone()

        return {"desc_cliente": result[0] if result else "Descripción de Cliente no encontrada"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
