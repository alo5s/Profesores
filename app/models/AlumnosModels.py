from ..database.db import get_db_connection


class AlumnoModel():

    # Alumnos
    @staticmethod
    def views_Alumnos():
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "SELECT  * FROM alumnos"
                cursor.execute(sql)
                datos = cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return datos
    
    # Grupo
    @staticmethod
    def views_grupos():
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "SELECT  * FROM grupos"
                cursor.execute(sql)
                datos = cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return datos
    
    # VISTA DE CLASES DE ALUMNO
    @staticmethod
    def viws_clases_alumnos(id):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "SELECT * FROM alumnos WHERE id= %s"
                cursor.execute(sql, (id,))
                alumno = cursor.fetchall()

                query = "SELECT * FROM clase_alumno WHERE alumno_id= %s"
                cursor.execute(query, (id,))
                clases = cursor.fetchall()

        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return alumno, clases
    

    # VISTA DE CLASES DE GRUPO
    @staticmethod
    def viws_clases_grupo(id):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "SELECT * FROM grupos WHERE id= %s"
                cursor.execute(sql, (id,))
                alumno = cursor.fetchall()

                query = "SELECT * FROM clase_grupos WHERE  grupo_id= %s"
                cursor.execute(query, (id,))
                clases = cursor.fetchall()

        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return alumno, clases
    