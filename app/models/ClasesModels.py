from ..database.db import get_db_connection


class ClasesModel():

    @staticmethod
    def add_clases_alumno(dato):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "INSERT INTO clase_alumno (tema, descripcion, tiempo, fecha, alumno_id, profesor_id, validacion) VALUES(%s, %s ,%s, %s, %s, %s, %s)" 
                cursor.execute(sql, (dato[0][2], dato[0][3], dato[0][0], dato[0][1], dato[1], dato[2], False))
                affected_rows = cursor.rowcount
                conn.commit() 

        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return affected_rows
    
    @staticmethod
    def add_clases_grupo(dato):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "INSERT INTO clase_grupos (tema, descripcion, tiempo, fecha, grupo_id, profesor_id, validacion) VALUES(%s, %s, %s, %s, %s, %s, %s)" 
                cursor.execute(sql, (dato[0][2], dato[0][3], dato[0][0], dato[0][1], dato[1], dato[2], False))
                affected_rows = cursor.rowcount
                conn.commit() 

        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return affected_rows
