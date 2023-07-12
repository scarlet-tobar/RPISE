import psycopg2

def postgres_connection():
    host = 'se.skrlet13.xyz'
    database = 'embebidos'
    user = 'postgres'
    password = 'embebidos'

    try:
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        print('Conexión exitosa')
        return connection

    except (Exception, psycopg2.Error) as error:
        print('Error al conectar con PostgreSQL:', error)
        return None
