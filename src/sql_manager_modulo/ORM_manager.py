from dataclasses import dataclass
from typing import Dict, Any, Iterable
import pandas as pd
from sqlalchemy import create_engine, inspect
import urllib
import pyodbc
import dotenv
import os
import pymssql
import logging

dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
class ConnectionSettings:

    def __init__(self, server, database, username, password, driver) -> None:
        self.server: str = server
        self.database: str = database
        self.username: str = username
        self.password: str = password
        self.driver: str = driver
        self.timeout: int = 600
    def __str__(self):
        return f'{self.server}\n{self.database}\n{self.username}\n{self.password}\n{self.driver}\n{self.timeout}'

def azureDBparams() -> ConnectionSettings:
    server: str = f"{os.getenv('AZserver')}"
    database: str = f"{os.getenv('AZdatabase')}"
    username: str = f"{os.getenv('AZusername')}"
    password: str = f"{os.getenv('AZpassword')}"
    driver: str = 'ODBC Driver 17 for SQL Server'
    parametros_azure = ConnectionSettings(server,database,username,password,driver)
    return parametros_azure

def localDBparams() -> ConnectionSettings: 
    server: str = f"{os.getenv('local_server')}"
    database: str = f"{os.getenv('local_database')}"
    username: str = f"{os.getenv('local_username')}"
    password: str = f"{os.getenv('local_password')}"
    driver: str = 'ODBC Driver 17 for SQL Server'
    parametros_locales = ConnectionSettings(server,database,username,password,driver)
    return parametros_locales

class DBconnection:
    """
    Azure SQL database connection.
    """
    def __init__(self, conn_settings: ConnectionSettings, echo: bool = False) -> None:
        params = urllib.parse.quote_plus(
            f'DRIVER={conn_settings.driver};'
            f'SERVER={conn_settings.server};'
            f'DATABASE={conn_settings.database};'
            f'UID={conn_settings.username};'
            f'PWD={conn_settings.password};'
            'Trusted_Connection=no;'
        )
        conn_string = f'mssql+pyodbc:///?odbc_connect={params}'
        self.db = create_engine(conn_string, echo=echo)
    def connect(self) -> None:
        """Estimate connection."""  
        self.conn = self.db.connect()

    def get_tables(self) -> Iterable[str]:
        """Get list of tables."""
        inspector = inspect(self.db)
        return [t for t in inspector.get_table_names()]

    def dispose(self) -> None:
        """Dispose opened connections."""
        self.conn.close()
        self.db.dispose()

def extraer_dim_camaras() -> pd.DataFrame:
    """extrae los datos de la tabla dispositivos en un dataframe"""
    parametros = azureDBparams()
    db_conn = DBconnection(parametros)
    db_conn.connect()
    pull_query = 'SELECT * FROM DISPOSITIVO WHERE DISPOSITIVO.IP_ADDRESS IS NOT NULL'
    try:
        query_df = pd.read_sql_query(pull_query, db_conn.conn)
        return query_df
    except Exception as e:
        logger.error(f"Error obteniendo datos de sql:\n{e}")
    finally:
        db_conn.dispose()

def push_to_DB(df: pd.DataFrame,table_name:str, params:ConnectionSettings) -> None:
    """crea un insert con un dataframe
    input: pd.dF, nombre de tabla: str, parametros de conexión: ConnectionSettings"""
    db_conn = DBconnection(params)
    db_conn.connect()
    schema='dbo'
    if_exists='append'
    index=False
    try:
        with db_conn.conn.begin() as trans:  
            df.to_sql(
                table_name,
                con=db_conn.conn,
                schema=schema,
                if_exists=if_exists,
                index=index,
                chunksize=1000, 
                method='multi')
        
        logger.info("Datos insertados correctamente en {schema}.{table_name}")
    except pyodbc.ProgrammingError as e:
        logger.error(f"Error de programación (¿columnas no coinciden?): {str(e)}")
        raise
    except pyodbc.OperationalError as e:
        logger.error(f"Error operacional (¿problema de conexión?): \n{str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        raise
    finally:
        db_conn.dispose()

def query_db(query:str,params:ConnectionSettings) -> bool:
    """Envía query a bbdd y la retorna en forma de bool si es insert
    o pd.DataFrame si es query"""
    db_conn = DBconnection(params)
    db_conn.connect()
    try:
        resultset = pd.read_sql_query(query, db_conn.conn)
    except pyodbc.ProgrammingError as e:
        logger.error(f"Error de programación (¿columnas no coinciden?): {str(e)}")
        raise
    except pyodbc.OperationalError as e:
        logger.error(f"Error operacional (¿problema de conexión?): \n{str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        raise
    finally:
        db_conn.dispose()
        return resultset

if __name__ == "__main__":

    parametros_azure = azureDBparams()
    parametros_locales = localDBparams()
    
    db_conn = DBconnection(parametros_locales)
    db_conn.connect()

    pull_query = 'SELECT DISPOSITIVO_ID, IP_ADDRESS FROM [dbo].DISPOSITIVO'
    try:
        for t in db_conn.get_tables():
            print(t)
        resultset = pd.read_sql_query(pull_query, db_conn.conn)
        print(resultset.head())
    finally:
        db_conn.dispose()

