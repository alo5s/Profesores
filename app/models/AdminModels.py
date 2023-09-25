# Importamos la conexión de la base de dato,
#from database.db import get_db_connection
from ..database.db import get_db_connection

# Contraseña 
pw = "Hola buenos días esto es la contraseña"
ha = "2239f2cf390a969b1262b74934ea0bad"

class AdminModel():
    @staticmethod
    def get_usuario_por_nombre(usuario):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "SELECT * FROM usuario_admin WHERE usuario = %s"
                cursor.execute(sql, (usuario,))
                user_data = cursor.fetchone()
                if user_data:
                    return {
                        'admin': True,
                        'usuario': user_data[0],
                        'contraseña': user_data[1]
                    }
                return None
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()


    # Profesores

    @staticmethod
    def views_profesores():
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = """
                    SELECT profesores.*, 
                        COUNT(DISTINCT CASE WHEN clase_alumno.validacion = FALSE THEN clase_alumno.id END) + 
                        COUNT(DISTINCT CASE WHEN clase_grupos.validacion = FALSE THEN clase_grupos.id END) AS "Total Clases",
                        SUM(CASE WHEN clase_alumno.validacion = FALSE THEN clase_alumno.tiempo ELSE 0 END
                           + CASE WHEN clase_grupos.validacion = FALSE THEN clase_grupos.tiempo ELSE 0 END) AS tiempo_total
                    FROM profesores
                    LEFT JOIN clase_alumno ON profesores.id = clase_alumno.profesor_id
                    LEFT JOIN clase_grupos ON profesores.id = clase_grupos.profesor_id
                    GROUP BY profesores.id
                    """
                cursor.execute(sql)
                datos = cursor.fetchall()
                
                #sql = """
                #SELECT profesores.id,
                #       SUM(CASE WHEN clase_alumno.validacion = FALSE THEN clase_alumno.tiempo ELSE 0 END
                #           + CASE WHEN clase_grupos.validacion = FALSE THEN clase_grupos.tiempo ELSE 0 END) AS tiempo_total
                #FROM profesores
                #LEFT JOIN clase_alumno ON profesores.id = clase_alumno.profesor_id
                #LEFT JOIN clase_grupos ON profesores.id = clase_grupos.profesor_id
                #GROUP BY profesores.id
                #"""
                #cursor.execute(sql)
                #datos_1 = cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return datos
    

    @staticmethod
    def viws_clases_profesor(id):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                query = """
                    SELECT clase_alumno.*, 'estudiante' AS tipo, CONCAT(alumnos.nombre, ' ', alumnos.apellido) AS nombre_estudiante
                    FROM clase_alumno
                    JOIN alumnos ON clase_alumno.alumno_id = alumnos.id
                    WHERE clase_alumno.profesor_id = %s 
                    """
                cursor.execute(query, (id,))
                data_alumno = cursor.fetchall()
 
                query = """
                    SELECT clase_grupos.*, 'grupo' AS tipo, grupos.nombre AS nombre
                    FROM clase_grupos
                    JOIN grupos ON clase_grupos.grupo_id = grupos.id
                    WHERE clase_grupos.profesor_id = %s
                    """
                cursor.execute(query, (id,))
                data_grupo = cursor.fetchall()

                datos = data_alumno + data_grupo

        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return datos


    @staticmethod
    def validado_profesor_alumno(id):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "UPDATE clase_alumno SET validacion = True WHERE id = %s"
                cursor.execute(sql, (id,))
                affected_rows = cursor.rowcount
                conn.commit()
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return affected_rows
    

    @staticmethod
    def validado_profesor_grupo(id):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "UPDATE clase_grupos SET validacion = True WHERE id = %s"
                cursor.execute(sql, (id,))
                affected_rows = cursor.rowcount
                conn.commit()
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return affected_rows




    @staticmethod
    def add_profesor(dato):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "INSERT INTO profesores (fullname, contraseña) VALUES(%s, %s)"
                cursor.execute(sql, (dato[0],dato[1]))
                affected_rows = cursor.rowcount
                conn.commit() 

        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return affected_rows
    
    @staticmethod
    def delete_profesor(id):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "DELETE FROM profesores WHERE  id = %s "
                cursor.execute(sql, (id,))
                affected_rows = cursor.rowcount
                conn.commit() 
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return affected_rows
    
    @staticmethod
    def update_profesor(dato,id):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "UPDATE profesores SET fullname = %s, contraseña = %s WHERE id = %s"
                cursor.execute(sql, (dato[0],dato[1], id))
                affected_rows = cursor.rowcount
                conn.commit() 
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return affected_rows
    


    # Alumno
    @staticmethod
    def views_alumnos():
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                #sql = "SELECT  * FROM alumnos"
                sql = """
                SELECT alumnos.*, COUNT(clase_alumno.id) AS total_clases
                FROM alumnos
                LEFT JOIN clase_alumno ON alumnos.id = clase_alumno.alumno_id
                GROUP BY alumnos.id, alumnos.nombre, alumnos.apellido
                """
                cursor.execute(sql)
                datos = cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return datos



    @staticmethod
    def viws_clases_alumno(id):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                query = """
                    SELECT clase_alumno.*, profesores.fullname AS nombre_profesor, clase_alumno.validacion
                    FROM clase_alumno
                    JOIN profesores ON clase_alumno.profesor_id = profesores.id

                    WHERE clase_alumno.alumno_id = %s 
                    """
                cursor.execute(query, (id,))
                datos = cursor.fetchall()
 
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return datos


    @staticmethod
    def delete_clases_alumno(id):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "DELETE FROM clase_alumno WHERE  id = %s "
                cursor.execute(sql, (id,))
                affected_rows = cursor.rowcount
                conn.commit() 
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return affected_rows
    

    @staticmethod
    def add_alumno(dato):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "INSERT INTO alumnos (nombre, apellido) VALUES(%s, %s)"
                cursor.execute(sql, (dato[0],dato[1]))
                affected_rows = cursor.rowcount
                conn.commit() 

        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return affected_rows
    
    @staticmethod
    def delete_alumno(id):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "DELETE FROM alumnos WHERE  id = %s "
                cursor.execute(sql, (id,))
                affected_rows = cursor.rowcount
                conn.commit() 
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return affected_rows
    
    @staticmethod
    def update_alumno(dato,id):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "UPDATE alumnos SET nombre = %s, apellido = %s WHERE id = %s"
                cursor.execute(sql, (dato[0],dato[1], id))
                affected_rows = cursor.rowcount
                conn.commit() 
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return affected_rows
    
    # Grupos
    @staticmethod
    def views_grupos():
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "SELECT  * FROM grupos"
                sql = """
                SELECT grupos.*, COUNT(clase_grupos.id) AS total_clases
                FROM grupos
                LEFT JOIN clase_grupos ON grupos.id = clase_grupos. grupo_id
                GROUP BY grupos.id, grupos.nombre
                """
                cursor.execute(sql)
                datos = cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return datos



    @staticmethod
    def add_grupo(dato):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "INSERT INTO grupos (nombre, integrantes) VALUES(%s, %s)"
                cursor.execute(sql, (dato[0],dato[1]))
                affected_rows = cursor.rowcount
                conn.commit() 

        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return affected_rows
    
    @staticmethod
    def delete_grupo(id):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "DELETE FROM grupos WHERE  id = %s "
                cursor.execute(sql, (id,))
                affected_rows = cursor.rowcount
                conn.commit() 
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return affected_rows
    
    @staticmethod
    def update_grupo(dato,id):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "UPDATE grupos SET nombre = %s, integrantes = %s WHERE id = %s"
                cursor.execute(sql, (dato[0],dato[1], id))
                affected_rows = cursor.rowcount
                conn.commit() 
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return affected_rows
    

    @staticmethod
    def viws_clases_grupo(id):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                query = """
                    SELECT clase_grupos.*, profesores.fullname AS nombre_profesor, clase_grupos.validacion
                    FROM clase_grupos
                    JOIN profesores ON clase_grupos.profesor_id = profesores.id

                    WHERE clase_grupos.grupo_id = %s 
                    """
                cursor.execute(query, (id,))
                datos = cursor.fetchall()
 
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return datos


    @staticmethod
    def delete_clases_grupo(id):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "DELETE FROM clase_grupos WHERE  id = %s "
                cursor.execute(sql, (id,))
                affected_rows = cursor.rowcount
                conn.commit() 
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()
        return affected_rows
    