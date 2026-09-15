import os
from models.database import obtener_conexion

DB_PRODUCTOS = os.getenv("DB_DATABASE")
if not DB_PRODUCTOS:
    raise RuntimeError("Falta la variable de entorno DB_DATABASE")

def guardar_historico_pesaje(datos: dict) -> None:
   
    sql = f"""
        INSERT INTO [{DB_PRODUCTOS}].dbo.hstrco_psje (
            nmro_psta, prcso, cdgo_plu, nmbre_plu, tpo_lmpza, nmro_lte,
            fcha_prdccion, fcha_vnce_ref, fcha_vnce_cong, fcha_scrfcio,
            pso_nto, pso_tra, pso_brto, cdgo_emprsa, pddo, prcndor,
            actlzcion, oprdor
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE(), ?)
    """
    valores = (
        datos.get("nmro_psta", 0),
        datos.get("prcso", 1),
        datos.get("cdgo_plu", 0),
        datos.get("nmbre_plu", ""),
        datos.get("tpo_lmpza", 0),
        datos.get("nmro_lte", 0),
        datos.get("fcha_prdccion", "1900-01-01"),
        datos.get("fcha_vnce_ref", "1900-01-01"),
        datos.get("fcha_vnce_cong", "1900-01-01"),
        datos.get("fcha_scrfcio", "1900-01-01"),
        datos.get("pso_nto", 0),
        datos.get("pso_tra", 0),
        datos.get("pso_brto", 0),
        datos.get("cdgo_emprsa", 0),
        datos.get("pddo", 0),
        datos.get("prcndor", 0),
        datos.get("oprdor", ""),
    )
    with obtener_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute(sql, valores)
        conexion.commit()
        cursor.close()
        
        