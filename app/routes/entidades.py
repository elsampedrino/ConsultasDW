from http.client import HTTPException
from fastapi import APIRouter, Query
from app.database.teradata_connection import get_teradata_connection
from app.database.sqlserver_connection import get_sqlserver_connection
from app.models.convenios_model import ConveniosEntes2
from app.models.entidades_model import EntPubPriv,RuitConv,RuitJurisd
from typing import List
import app.utils.helpers as helpers

router = APIRouter()

@router.get("/Entidades/EntPubPriv", response_model=List[EntPubPriv])
def obtener_ent_pubpri():
    try:
        conn = get_teradata_connection()
        cursor = conn.cursor()
        sql = """
            SELECT
            E.cod_convenio_entidad AS COD_ENTE,E.cod_sub_convenio_entidad AS cod_subente,E.desc_convenio_entidad AS descrip_ente,
            D.num_identif_tributaria AS cuit_ente,C.cod_ubicacion AS suc_cta,C.id_d_producto AS prod_cta,C.num_cuenta AS num_cta,
            E.fec_inicio_actividad_entidad AS fec_inicio_act,E.fec_fin_actividad_entidad AS fec_fin_act,
            CASE
            WHEN E.cod_clasificacion_ente = 10 THEN 'Privado'
            WHEN E.cod_clasificacion_ente = 20 THEN 'Público'
            WHEN E.cod_clasificacion_ente = 21 THEN 'Público Nacional'
            WHEN E.cod_clasificacion_ente = 22 THEN 'Público Provincial'
            WHEN E.cod_clasificacion_ente = 23 THEN 'Público Municipal'
            ELSE ' ' END AS clasif_ente,
            CASE
            WHEN E.cod_modo_captura_recaudacion = 0 THEN 'Caja'
            WHEN E.cod_modo_captura_recaudacion = 1 THEN 'Back Office'
            WHEN E.cod_modo_captura_recaudacion = 2 THEN 'Caja(Entes Generales)'
            ELSE ' ' END AS modo_capt,
            CASE
            WHEN E.cod_forma_acreditacion_entidad = 1 THEN 'Cta Propia'
            WHEN E.cod_forma_acreditacion_entidad = 2 THEN 'Mep'
            WHEN E.cod_forma_acreditacion_entidad = 3 THEN 'Rubro Contable'
            ELSE ' ' END AS forma_acred,
            E.cod_concepto_liquidacion AS conc_liquid,
            E.pct_calculo_comision AS porc_comi,
            E.val_minimo_comision AS min_comi,
            E.val_maximo_comision AS max_comi,
            E.val_alicuota_retencion AS porc_rete,
            E.val_archivo_respaldo AS form_arch_rend,
            E.val_listado_respaldo AS form_list_rend
            FROM p_sem_views.d_entes_entidades E
            LEFT JOIN p_sem_views.d_contratos_actual C
                ON C.id_d_contrato = E.id_d_contrato
            LEFT JOIN p_sem_views.d_clientes_actual D
                ON D.id_d_cliente = C.id_d_cliente
            WHERE E.fec_CALENDARIO = DATE -1
                AND E.cod_CONVENIO_ENTIDAD NOT IN ( 9997 , 9999 )
                AND E.fec_fin_actividad_entidad > DATE -1
                AND E.cod_modo_captura_recaudacion IN ( 0 , 2 )
            ORDER BY 1,2,3
        """
        cursor.execute(sql, ())
        results = helpers.query_to_dict_list(cursor)
        return results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en /Entidades/EntPubPriv: {str(e)}")        
    finally:
        cursor.close()
        conn.close()

@router.get("/Entidades/RuitConv", response_model=List[RuitConv])
def obtener_ent_ruitConv():
    try:
        conn = get_teradata_connection()
        cursor = conn.cursor()
        sql = """
            SELECT 
            C.id_d_convenio_ruit AS COD_CONVENIO,C.fec_calendario AS FEC_ALTA_CONVENIO,
            id_d_jurisdiccion_constatacion AS JUR_CONST,pct_jurisdiccion_constatacion AS PCT_CONST,
            num_formulario_ruit AS FORM_RUIT,num_autoridad_constatacion_ruit AS AUT_CONST,
            id_d_jurisdiccion AS JUR_RUIT,pct_jurisdiccion AS PCT_JUR
            FROM P_SEM_VIEWS.D_RENDICIONES_RUIT_CONVENIOS C
            INNER JOIN P_SEM_VIEWS.D_RENDICIONES_RUIT_PORCENTAJES P
                ON C.ID_D_CONVENIO_RUIT = P.ID_D_CONVENIO_RUIT
                AND P.FEC_CALENDARIO = DATE -1
            WHERE C.FEC_CALENDARIO = DATE -1
            ORDER BY C.ID_D_CONVENIO_RUIT,P.ID_D_JURISDICCION
        """
        cursor.execute(sql, ())
        results = helpers.query_to_dict_list(cursor)
        return results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en /Entidades/RuitConv: {str(e)}")        
    finally:
        cursor.close()
        conn.close()

@router.get("/Entidades/RuitJurisd", response_model=List[RuitJurisd])
def obtener_ent_ruitConv():
    try:
        conn = get_teradata_connection()
        cursor = conn.cursor()
        sql = """
            SELECT 
            R.ID_D_JURISDICCION AS NUM_JURISD,R.NOM_JURISIDICCION AS NOM_JURISD,
            R.FEC_ALTA_JURISIDICCION AS FEC_ALTA_JURISD,
            R.MTO_DISTRIBUCION_RUIT AS IMP_BASE_DIST,C.NUM_CBU
            FROM P_SEM_VIEWS.D_RENDICIONES_RUIT_MONTOS R
            LEFT JOIN P_SEM_VIEWS.F_CUENTAS_CBU C
                ON R.ID_D_CONTRATO = C.ID_D_CONTRATO
                AND C.FEC_CALENDARIO = DATE -1
            WHERE R.FEC_CALENDARIO = DATE -1
            AND R.ID_D_CONTRATO > 0
            ORDER BY R.ID_D_JURISDICCION
        """
        cursor.execute(sql, ())
        results = helpers.query_to_dict_list(cursor)
        return results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en /Entidades/RuitJurisd: {str(e)}")        
    finally:
        cursor.close()
        conn.close()

@router.get("/Entidades/ConveniosEntes2", response_model=List[ConveniosEntes2])
def obtener_convenios():
    try:
        conn = get_sqlserver_connection()
        cursor = conn.cursor()
        sql = """
            SELECT E.Id_Ente as cod_ente,E.Canal_Cobranza,E.Nombre_Cabecera,E.Tipo_Ente,E.Condicion_Registro_id as Condicion_Registro_id_ente,
            E.Fecha_Alta as fec_alta_ente,E.Fecha_Baja,D.Id_Diseño,D.Nombre_Diseño,D.Longitud_Diseño,D.Tipo_Importe,
            D.Fecha_Alta as fec_alta_diseño,D.ContieneDV,D.DesactivarControlDV,D.Condicion_Registro_id as Condicion_Registro_id_diseño
            FROM dbo.Entes E
            INNER JOIN dbo.Diseños D
	            ON E.Id_Ente = D.Id_Ente
        """
        cursor.execute(sql, ())
        results = helpers.query_to_dict_list(cursor)
        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en /Convenios/ConveniosEntes: {str(e)}")
    finally:
        cursor.close()
        conn.close()
