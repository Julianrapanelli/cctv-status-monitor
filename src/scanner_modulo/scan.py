from sql_manager_modulo import ORM_manager as ORM
import pandas as pd
import asyncio
from icmplib import async_multiping
import sqlalchemy
import subprocess
import re
import platform
import logging
from sqlalchemy import text

from icmplib import async_multiping, Host

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def check_device_status(df_addresses: pd.DataFrame) -> pd.DataFrame:
    """
    Chequea de manera asíncrona si las cámaras están funcionando o no.
    input:
        df_addresses: DataFrame conteniendo las dirección IP.
    output:
        DataFrame con la columna 'STATUS' acusando conexión o desconexión en boolean.
    """
    result_df = df_addresses.copy()
    
    try:
        unique_ips = result_df['IP_ADDRESS'].astype(str).unique()
        hosts: list[Host] = await async_multiping(unique_ips, privileged=False)
        status_map = {host.address: host.is_alive for host in hosts}
        result_df['STATUS'] = result_df['IP_ADDRESS'].astype(str).map(status_map).fillna(False)
        
        return result_df
    
    except Exception as e:
        logger.error(f"Error checking device status: {e}")
        return None

def scan():
    """
    Función para obtener y procesar datos de infraestructura.
    """
    try:
        # Retrieve infrastructure data from ORM
        df_infra = ORM.extraer_dim_camaras()
        print(df_infra.to_markdown(tablefmt="heavy_outline", stralign="left", numalign="left"))
        if df_infra is None or df_infra.empty:
            logger.warning("No se obtuvieron datos de infraestrcutura")
            return
        # Run async function in event loop
        status_df = asyncio.run(check_device_status(df_infra))

        # Log results
        logger.info("Chequeo de dispositivos listo.")
        print(status_df[['DISPOSITIVO_ID', 'IP_ADDRESS', 'STATUS']].head())
        print(f'{status_df.to_markdown(tablefmt="heavy_outline", stralign="left", numalign="left")}')
        #resultados -> .CSV
        #status_df.to_csv('device_status.csv', index=False)
        
        return status_df
    
    except Exception as e:
        logger.error(f"Error inesperado en proceso princial: {e}")
        return None

if __name__ == '__main__':
    
    parametros_azure = ORM.azureDBparams()

    """
    Inserta un nuevo registro scan en SCAN
    Escanea todos los dispositivos
    Compara los disp. desconectados en bbdd y si alguno volvió, los actualiza en la tabla DESCONEXION.
    Inserta los nuevos disp. sin conexión en la tabla DESCONEXION
    """
    #inserta nuevo scan en tabla scan
    el = pd.DataFrame({'SCAN_DATE': [sqlalchemy.text("DEFAULT")]})
    ORM.push_to_DB(el,'SCAN', parametros_azure)

    #recupera el último número de scan
    ult_scan_query = "SELECT TOP 1 SCAN_ID FROM SCAN ORDER BY SCAN_ID DESC;"
    ult_scan_id:pd.DataFrame = ORM.query_db(ult_scan_query, parametros_azure)
    scan_id:int = ult_scan_id.at[0,'SCAN_ID']

    #select desconexiones que tengan valores null en reconexion
    desconexion_actual_query = "SELECT DISPOSITIVO_ID FROM DESCONEXION WHERE RECONEXION_DATE IS NULL"
    df_desconexion_table = ORM.query_db(desconexion_actual_query, parametros_azure)

    #scaneo de camaras
    df_status:pd.DataFrame = scan()
    print(df_status.to_markdown(tablefmt="heavy_outline", stralign="left", numalign="left"))

    #crea id_list: list con las camaras que reconectaron comparando con las que estaban caídas.
    if  not df_desconexion_table.empty:
        mask_reconectar = df_status['DISPOSITIVO_ID'].isin(df_desconexion_table['DISPOSITIVO_ID']) & df_status['STATUS']
        df_reconectar = df_status[mask_reconectar]
        ids = df_reconectar['DISPOSITIVO_ID'].tolist()
        id_list:list = ', '.join(map(str, ids))

        update_query = f"""
            UPDATE [dbo].DESCONEXION
            SET RECONEXION_DATE = TODATETIMEOFFSET(SYSDATETIME(), '-03:00')
            WHERE DISPOSITIVO_ID IN ({id_list})
            AND RECONEXION_DATE IS NULL;
        """
        if not df_reconectar.empty:
            db_conn = ORM.DBconnection(parametros_azure)
            db_conn.connect()
            try:
                db_conn.conn.execute(text(update_query))
                db_conn.conn.commit()
                logger.info("Se actualizaron reconexiones correctamente.")
            except Exception as e:
                logger.error(f"Error actualizando reconexiones: {e}")
                db_conn.conn.rollback()
            finally:
                db_conn.dispose()   
    
    # Filtrar nuevos desconectados (busca los dispositivos desconectados que NO están 
    # en la bbdd y los guarda en df_new_desconexiones)
    desconexiones_cargadas = df_desconexion_table['DISPOSITIVO_ID'].unique()
    mask_new = (df_status['STATUS'] == False) & (~df_status['DISPOSITIVO_ID'].isin(desconexiones_cargadas))
    df_new_desconexiones = df_status[mask_new].copy()
    df_new_desconexiones['SCAN_ID'] = scan_id

    # Insertar solo columnas necesarias
    if not df_new_desconexiones.empty:
        ORM.push_to_DB(df_new_desconexiones[['DISPOSITIVO_ID', 'SCAN_ID']], 'DESCONEXION', parametros_azure)
