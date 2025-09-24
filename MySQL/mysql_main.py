import mysql.connector
from mysql.connector import Error
import os
def limpiar_pantalla():
    if os.name == 'nt':
        os.system('cls')

def conectar_mysql():
	try:
		conexion = mysql.connector.connect(
			host="localhost", # Servidor MySQL
			database="mysql_python", # Nombre de la base de datos
			user="root", # Nombre de usuario de MySQL
			password="root" # Contraseña de usuario de MySQL
		)

		if conexion.is_connected():
			print("Conexion exitosa a MySQL")
			info_servidor = conexion.get_server_info()
			print(f"Informacion del servidor: MySQL {info_servidor}")

			cursor = conexion.cursor()
			cursor.execute("SELECT DATABASE();")
			bd_actual = cursor.fetchone()
			print(f"Base de datos actual: {bd_actual[0]}")

			return conexion
		
	except Error as e:
		print(f"Error al conectar a MySQL: {e}")
		return None

def crear_tabla_usuario(conexion):
	try:
		cursor = conexion.cursor()

		crear_tabla = """
		CREATE TABLE usuarios (
		id INT AUTO_INCREMENT PRIMARY KEY,
		nombre VARCHAR(100) NOT NULL,
		email VARCHAR(100) UNIQUE NOT NULL,
		edad INT,
		fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)
		"""

		cursor.execute(crear_tabla)
		print("Tabla 'usuarios' creada o verificada correctamente")
	
	except Error as e:
		print(f"Error al crear tabla: {e}")

def insertar_usuario(conexion, nombre, email, edad):
	try:
		cursor = conexion.cursor()

		insertar_sql = "INSERT INTO usuarios (nombre, email, edad) VALUES (%s, %s, %s)"
		datos_usuario = (nombre, email, edad)

		cursor.execute(insertar_sql, datos_usuario)
		conexion.commit()

		print(f"Usuario '{nombre}' insertado correctamente (ID: {cursor.lastrowid}")
	except Error as e:
		print(f"Error al insertar usuario: {e}")

def consultar_usuarios(conexion):
	try:
		cursor = conexion.cursor()
		consulta_sql = "SELECT id, nombre, email, edad, fecha_creacion FROM usuarios"
		cursor.execute(consulta_sql)

		usuarios = cursor.fetchall()
		
		print("\nLista de usuarios:")
		print("┌"+ "─" * 82 + "┐") # Carácter "Box Drawing" (línea sólida)
		print(f"{'ID':<5} {'NOMBRE':<20} {'EMAIL':<30} {'EDAD':<5} {'FECHA CREACION'}") # para que sirve el :<5 ??? 

		for usuario in usuarios:
			id_usuario, nombre, email, edad, fecha = usuario
			print(f"{id_usuario:<5} {nombre:<20} {email:<30} {edad:<5} {fecha}")
		
		print("└"+ "─" * 82 + "┘") # Carácter "Box Drawing" (línea sólida)
		print(f"\nTotal de usuarios: {len(usuarios)}")

	except Error as e:
		print(f"Error al consultar usuarios: {e}")

def buscar_usuario_por_email(conexion, email_a_buscar):
	try:
		cursor=conexion.cursor()

		buscar_sql = "SELECT * FROM usuarios WHERE email = %s"
		cursor.execute(buscar_sql, (email_a_buscar,)) #????

		usuario = cursor.fetchone()

		if usuario:
			print(f"\nUsuario encontrado:")
			print(f"	ID: {usuario[0]}")
			print(f"	Nombre: {usuario[1]}")
			print(f"	Email: {usuario[2]}")
			print(f"	Edad: {usuario[3] or "N/A"}")
			print(f"	Fecha de creacion: {usuario[4]}")
		else:
			print(f"No se ha encontrado usuario con email: {email_a_buscar}")

	except Error as e:
		print(f"Error al buscar usuario por email: {e}")

def main():
	
	print("Programa iniciado")
	print("Ejemplo de conexion a MySQL")
	print("=" * 50)
	
	conexion = conectar_mysql()

	if conexion:
		try:
			crear_tabla_usuario(conexion)

			print("\nInsertando usuarios de ejemplo...")

			insertar_usuario(conexion, "Juan Pérez", "juan.perez@email.com", 25)
			insertar_usuario(conexion, "María González", "maria.gonzalez@email.com", 30)
			insertar_usuario(conexion, "Carlos Rodriguez", "carlos.rodriguez@email.com", 20)

			consultar_usuarios(conexion)

			print("\nBuscando usuario por Email...")

			email_a_buscar =input("Ingrese el email a buscar: ")
			buscar_usuario_por_email(conexion, email_a_buscar)

		except Exception as e:
			print(f"Error en operaciones: {e}")

		finally:
			if conexion.is_connected():
				conexion.close()
				print("\nConexion cerrada")
	else:
		print("No se pudo establecer conexion MySQL")
		print("\nVerifique:")
		print("- Que MySQL este ejecutandose")
		print("- Las credenciales de conexion")
		print("- Que exista la base de datos")

if __name__ == "__main__":
	limpiar_pantalla()
	main()
