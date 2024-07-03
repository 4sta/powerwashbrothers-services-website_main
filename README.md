# Power Wash Brothers Services Website

## Project Description

This project is a web application for "Power Wash Brothers," a company that provides cleaning services. The website includes the following features:
- **Service Information**: Pages with detailed descriptions of available cleaning services.
- **Customer Reviews**: A page displaying comany work.
- **FAQs**: A frequently asked questions page to help customers with common inquiries.
- **Service Order Form**: A form that allows customers to place orders for services, including reCAPTCHA for spam protection.
- **Admin Orders Page**: A hidden page for admin users to view all orders placed by customers.


## Installation

1. Clone the repository to your local machine: `git clone https://github.com/4sta/powerwashbrothers-services-website.git`
2. Navigate to the project directory: `cd powerwashbrothers-services-website`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - For Windows: `venv\Scripts\activate`
   - For macOS and Linux: `source venv/bin/activate`
5. Install the dependencies: `pip install -r requirements.txt`

## Environment Variables

Make sure to set the following environment variables in a `.env` file in the root directory of the project:
- `GCP_PROJECT_ID`
- `RECAPTCHA_SITE_KEY`
- `RECAPTCHA_SECRET_KEY`
- `MAIL_SERVER`
- `MAIL_PORT`
- `MAIL_USE_TLS`
- `MAIL_USERNAME`
- `MAIL_PASSWORD`
- `MAIL_DEFAULT_SENDER`
- `ADMIN_ROUTE`
- `DATABASE_URL`

## Running the Application

To run the application locally, use the following command: `python app.py`

The application will be available at `http://127.0.0.1:5000`.

## Testing

To run the tests, use the following command: `pytest`

## Project Structure

- `app.py`: Main application file.
- `database.py`: Contains functions to interact with the database.
- `email_templates.py`: Contains email templates for order confirmations.
- `logging_config.py`: Configures logging for the application.
- `validation.py`: Contains form validation logic.
- `templates/`: Directory containing HTML templates.
- `static/`: Directory containing static files (CSS, JavaScript, images).
- `tests/`: Directory containing test files.

## Asynchronous Email Sending

To improve performance and avoid blocking the main thread, the application uses threading to send emails asynchronously.

## Admin Orders Page

The application includes a temporary hidden route for admin to view all orders.

## Deploy

This website is running with the help of render.com to see the site live visit `(https://powerwashbrothers.onrender.com)`.