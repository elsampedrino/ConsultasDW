from fastapi import APIRouter, HTTPException
from app.database.sqlserver_connection import get_sqlserver_connection
#from app.models.convenios_model import ConveniosEntes
from typing import List
import app.utils.helpers as helpers

router = APIRouter()

@router.get("/Convenios/Entes")
def obtener_entes_convenios():
    try:
        conn = get_sqlserver_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Id_Ente, Nombre_Corto FROM dbo.Entes WHERE Fecha_Baja IS NULL")
        entes = [{"id_ente": row.Id_Ente, "nombre_corto": row.Nombre_Corto} for row in cursor.fetchall()]
        return entes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener Entes: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/Convenios/DiseniosPorEnte")
def obtener_disenios_por_ente(id_ente: int):
    try:
        conn = get_sqlserver_connection()
        cursor = conn.cursor()

        query = """
            SELECT id_diseño, nombre_diseño, longitud_diseño, fecha_alta, fecha_Baja,
            Descripcion, contienedv, desactivarcontroldv 
            FROM dbo.Diseños D
	        INNER JOIN dbo.Maestro_Tipo_Importe M
	            ON D.Tipo_Importe = M.Id_Tipo_Importe
            WHERE Id_Ente = ? AND (Fecha_Baja IS NULL OR Fecha_Baja > GETDATE())
        """
        cursor.execute(query, id_ente)
        disenios = helpers.query_to_dict_list(cursor)
        return disenios
        #cursor.execute(query, (id_ente,))
        #rows = cursor.fetchall()
        #columns = [column[0] for column in cursor.description]

        #disenios = [dict(zip(columns, row)) for row in rows]
        #return disenios
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener Diseños de Entes: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/Convenios/DetallePorDisenio")
def obtener_detalle_por_disenio(
    id_ente: int,
    id_diseño: int
):
    try:
        conn = get_sqlserver_connection()
        cursor = conn.cursor()

        # Detalles Diseños
        query = """
            SELECT nombre,desde,longitud,valores_admitidos,mínimos_maximos,detectable,
            case D.Id_Contenido 
				when 0 then '' 
				else C.Descripcion end as descripcion,
            posicion_identificador,tipo_DV,condicion_registro_id,fecha_alta,fecha_baja
            FROM dbo.Detalles_Diseños D
	        INNER JOIN dbo.Contenidos C
		        on D.Id_Contenido = C.Id_Contenido
            WHERE Id_Ente = ? AND id_diseño = ? AND Fecha_Baja IS NULL
        """
        cursor.execute(query, (id_ente, id_diseño))
        detalles_disenios = helpers.query_to_dict_list(cursor)
        
        # Configuración Cobranza
        query = """
            SELECT cob_efec,cob_ch,cob_ch_varios,débito,debcre_pesos,debcre_dolar,cobro_1venc,cobro_2venc,cobro_3venc,
            cant_copias_ticket,dias_de_gracia1,dias_de_gracia2,dias_de_gracia3,dias_de_ghabil,control_duplicados,
            condicion_registro_id,fecha_alta,fecha_baja
            FROM dbo.Configuracion_Cobranza	        
            WHERE Id_Ente = ? AND id_diseño = ? AND Fecha_Baja IS NULL
        """
        cursor.execute(query, (id_ente, id_diseño))
        config_cobranza = helpers.query_to_dict_list(cursor)
        #cursor.execute("SELECT * FROM dbo.Configuracion_Cobranza WHERE Id_Ente = ? AND id_diseño = ? AND Fecha_Baja IS NULL", id_ente, id_diseño)
        #config_cobranza = [dict(zip([col[0] for col in cursor.description], row)) 
        #                   for row in cursor.fetchall()]

        return {
            "detalles_disenios": detalles_disenios,
            "configuracion_cobranza": config_cobranza
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener Detalles por Diseño: {str(e)}")
    finally:
        cursor.close()
        conn.close()
