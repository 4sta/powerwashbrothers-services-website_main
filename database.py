import os
import psycopg2

# connection to the database 

def get_services_db():
    try:
        db_conn = psycopg2.connect(os.environ['DATABASE_URL'])
        cursor = db_conn.cursor()

    
        cursor.execute(
            "SELECT id, title, information, important, price FROM services")
        services = cursor.fetchall()

  
        cursor.close()
        db_conn.close()

   
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
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return []


# connection based on the service id

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


# function to send orders to the database
def save_order_to_db(full_name, email, tel, service_type, work_object_details, remark):
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO orders (full_name, email, tel, service_type, work_object_details, remark)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (full_name, email, tel, service_type, work_object_details, remark))
        conn.commit()
        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Database error: {e}")