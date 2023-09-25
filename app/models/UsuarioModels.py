from ..database.db import get_db_connection


class UsuarioModel():
    @staticmethod
    def get_usuario_por_nombre(usuario):
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = "SELECT id, fullname, contraseña FROM profesores WHERE fullname = %s"
                cursor.execute(sql, (usuario,))
                user_data = cursor.fetchone()
                if user_data:
                    return {
                        'admin': False,
                        'id': user_data[0],
                        'fullname': user_data[1],
                        'contraseña':user_data[2]
                    }
                return None
        except Exception as ex:
            raise Exception(ex)
        finally:
            conn.close()