import psycopg2

def postgres_connection():
    host = 'localhost'
    database = 'embebidos'
    user = 'pi'
    password = 'raspberry'

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
