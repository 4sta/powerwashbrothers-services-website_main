import os
import psycopg2
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Function to get services from the database
def get_services_db():
    try:
        db_conn = psycopg2.connect(os.environ['DATABASE_URL'])
        cursor = db_conn.cursor()
        cursor.execute("SELECT id, title, information, important, price FROM services")
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

        logger.info("Fetched services from database")
        return services_list
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        return []

# Function to get a specific service by its ID from the database
def get_service_db(id):
    try:
        with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, title, information, important, price FROM services WHERE id = %s",
                    (id, ))
                service = cursor.fetchone()
                if service:
                    service_dict = {
                        'id': service[0],
                        'title': service[1],
                        'information': service[2],
                        'important': service[3],
                        'price': service[4]
                    }
                    logger.info(f"Fetched service with ID: {id} from database")
                    return service_dict
                logger.warning(f"Service with ID: {id} not found in database")
                return None
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        return None

# Function to save an order to the database
def save_order_to_db(full_name, email, tel, service_type, work_object_details, remark):
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO orders (full_name, email, tel, service_type, work_object_details, remark)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (full_name, email, tel, service_type, work_object_details, remark))
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Saved order for {full_name} into the database")
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")

# Function to get reviews from the database
def get_reviews():
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        cursor = conn.cursor()
        cursor.execute("SELECT id, image_url, caption FROM reviews")
        reviews = cursor.fetchall()

        reviews_list = []
        for review in reviews:
            review_dict = {
                'id': review[0],
                'image_url': review[1],
                'caption': review[2]
            }
            reviews_list.append(review_dict)

        cursor.close()
        conn.close()

        logger.info("Fetched reviews from database")
        return reviews_list
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return []
