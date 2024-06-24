import os
import psycopg2


# connecting to datab
def get_services_db():
  
    db_conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cursor = db_conn.cursor()

    # getting services from database
    cursor.execute(
        "SELECT id, title, information, important, price FROM services")
    services = cursor.fetchall()

    # closed cursor and connection
    cursor.close()
    db_conn.close()

    # list
    services_list = []
    for service in services:
        service_dict = {
            'id': service[0],
            'title': service[1],
            'information': service[2],
            'important': service[3],
            'price': service[4]
        }
        services_list.append(service_dict)

    return services_list



def get_service_db(id):
    try:
        with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, title, information, important, price FROM services WHERE id = %s",
                    (id,))
                service = cursor.fetchone()
                if service:
                    service_dict = {
                        'id': service[0],
                        'title': service[1],
                        'information': service[2],
                        'important': service[3],
                        'price': service[4]
                    }
                    return service_dict
                return None
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return None
