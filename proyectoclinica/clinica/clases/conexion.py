import pymysql

class Conexion:
    def obtener_conexion(self):
        return pymysql.connect(host='localhost',
                                user='root',
                                password='Misterpandita123.',
                                db='clinica',
                                )
