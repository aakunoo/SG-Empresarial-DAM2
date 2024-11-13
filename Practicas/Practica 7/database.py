import psycopg2

# Conexión a la base de datos dvdrental
conexion = psycopg2.connect(dbname="dvdrental", user="postgres", password="postgres")

cursor = conexion.cursor()
print("Conexión establecida con la base de datos 'dvdrental'.")

# 1. Pedir duración máxima por teclado
duracion_maxima = int(input("Introduce la duración máxima de las películas: "))

# 2. Seleccionar título, características especiales y duración de películas con duración menor a la indicada
consulta_peliculas = """SELECT title, special_features, length FROM film WHERE length < %s;"""
cursor.execute(consulta_peliculas, (duracion_maxima,))

# 3. Obtener y visualizar solo el primer registro
primer_registro = cursor.fetchone()
if primer_registro:
    print("\nPrimer registro seleccionado:")
    print("Título:", primer_registro[0])
    print("Características especiales:", primer_registro[1])
    print("Duración:", primer_registro[2])

# 4. Obtener y visualizar todos los registros restantes
registros = cursor.fetchall()
print("\nTodos los registros seleccionados:")
for registro in registros:
    print(registro)

# 5. Pedir datos del cliente y almacenarlos en una tupla
id_cliente = int(input("\nIntroduce el id del cliente: "))
nombre_cliente = input("Introduce el nombre del cliente: ")
apellido_cliente = input("Introduce el apellido del cliente: ")
email_cliente = input("Introduce el correo electrónico del cliente: ")
store_id = 1
address_id = 1

cliente_data = (id_cliente, store_id, address_id, nombre_cliente, apellido_cliente, email_cliente)
print(cliente_data)

# 6. Insertar nuevo cliente en la tabla customer
insertar_cliente = """INSERT INTO customer (customer_id, store_id, address_id, first_name, last_name, email) VALUES (%s, %s, %s, %s, %s, %s);"""
cursor.execute(insertar_cliente, cliente_data)
print("Cliente insertado correctamente.")

# 7. Actualizar el correo electrónico del cliente con ID 601
nuevo_email = "cliente@servidor.com"
actualizar_cliente = """UPDATE customer SET email = %s WHERE customer_id = %s;"""
cursor.execute(actualizar_cliente, (nuevo_email, 601))
print("Correo del cliente actualizado correctamente.")

# 8. Confirmar las transacciones
try:
    conexion.commit()
    print("Transacciones confirmadas.")
except Exception as e:
    print("Error al confirmar las transacciones:", e)
    conexion.rollback()
    print("Rollback realizado.")

# 9. Seleccionar y mostrar todos los registros de clientes
cursor.execute("SELECT * FROM customer;")
clientes = cursor.fetchall()
print("\nClientes registrados:")
for cliente in clientes:
    print(cliente)


# 10. Eliminar el registro de cliente creado
cliente_id = 601
try:
    eliminar_cliente = "DELETE FROM customer WHERE customer_id = %s;"
    cursor.execute(eliminar_cliente, (cliente_id,))
    print(f"Cliente con ID {cliente_id} eliminado correctamente.")

    # 11. Confirmar eliminación y manejo de excepciones
    conexion.commit()
    print("Transacciones confirmadas tras la eliminación.")
except Exception as e:
    print("Error al eliminar el cliente:", e)
    conexion.rollback()
    print("Rollback realizado.")

# 12. Mostrar todos los clientes para verificar la eliminación
cursor.execute("SELECT * FROM customer;")
clientes = cursor.fetchall()
print("\nClientes registrados después de la eliminación:")
for cliente in clientes:
    print(cliente)

# 13. Cerrar la conexión
cursor.close()
conexion.close()
print("Conexión con la base de datos cerrada.")