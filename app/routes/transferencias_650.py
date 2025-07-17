from fastapi import APIRouter, HTTPException, Query
from app.models.lotes_model import Lote650, DetLote650, Prod650Vig, OrdenanteDesc
from app.database.teradata_connection import get_teradata_connection
from typing import List
import app.utils.helpers as helpers

router = APIRouter()

@router.get("/Transferencias650/Lotes650", response_model=List[Lote650])
def obtener_lotes650(
    cod_ordenante: str = Query(...),
    fec_ini_pago: str = Query(...),
    fec_fin_pago: str = Query(...)
):
    try:
        conn = get_teradata_connection()
        cursor = conn.cursor()
        sql = """
                SELECT COD_ORDENANTE, ID_OPERACION, FEC_PAGO, IMP_CESION, CANT_TRANS
                FROM P_SEM_VIEWS.F_PAGO_HABERES_CABECERA
                WHERE COD_ORDENANTE = ?
                AND FEC_PAGO BETWEEN ? AND ?
                ORDER BY FEC_PAGO, ID_OPERACION
            """
        cursor.execute(sql, (cod_ordenante, fec_ini_pago, fec_fin_pago))
        results = helpers.query_to_dict_list(cursor)
        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en /Lotes650: {str(e)}")
    finally:
        cursor.close()
        conn.close()
    
    
@router.get("/Transferencias650/DetLote650", response_model=List[DetLote650])
def obtener_det_lote650(
    cod_ordenante: str = Query(...),
    fec_ini_pago: str = Query(...),
    fec_fin_pago: str = Query(...)
):
    try:
        conn = get_teradata_connection()
        cursor = conn.cursor()
        sql = """
                SELECT C.COD_ORDENANTE, C.ID_OPERACION, C.FEC_PAGO, C.IMP_CESION, C.CANT_TRANS,
                D.NUM_ORDEN, D.IMP_ORDEN, D.NUM_CBU_DESTINO
                FROM P_SEM_VIEWS.F_PAGO_HABERES_CABECERA C
                INNER JOIN P_SEM_VIEWS.F_PAGO_HABERES_DETALLE D
                ON C.ID_OPERACION = D.ID_OPERACION
                AND C.ID_D_CONTRATO = D.ID_D_CONTRATO
                WHERE C.COD_ORDENANTE = ?
                AND C.FEC_PAGO BETWEEN ? AND ?
                ORDER BY C.FEC_PAGO, C.ID_OPERACION, D.NUM_ORDEN
            """
        cursor.execute(sql, (cod_ordenante, fec_ini_pago, fec_fin_pago))
        results = helpers.query_to_dict_list(cursor)
        return results

        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en /DetLote650: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/Transferencias650/Prod650Vig", response_model=List[Prod650Vig])
def obtener_prod_650Vig(
    cuit: str = Query(...)
):
    try:
        conn = get_teradata_connection()
        cursor = conn.cursor()
        cursor.execute("CALL SB_OPERATIONAL.SP_PROD650_VIG(?)", (cuit,))
        cursor.execute("SELECT * FROM SB_OPERATIONAL.TMP_PROD650_VIG ORDER BY FEC_ALTA_CONTRATO")
        results = helpers.query_to_dict_list(cursor)
        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en /Prod650Vig: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/Transferencias650/OrdenanteDesc", response_model=OrdenanteDesc)
def obtener_descrip_ordenante(cuit: str = Query(...)):
    try:
        conn = get_teradata_connection()
        cursor = conn.cursor()

        sql = """
            SELECT NOM_CLIENTE FROM P_SEM_VIEWS.D_CLIENTES_ACTUAL WHERE NUM_IDENTIF_TRIBUTARIA = ?
            AND ID_D_CLIENTE < 100000000
        """
        cursor.execute(sql, (cuit,))
        result = cursor.fetchone()

        return {"desc_ordenante": result[0] if result else "Descripción de Ordenante no encontrada"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
