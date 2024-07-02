import pytest
from app import app as flask_app, send_email, admin_email_template, user_email_template, verify_recaptcha
from flask_mail import Mail, Message
import os
import requests
from unittest.mock import patch
from validation import validate_order_form

# This fixture provides a test client for our Flask app
@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

# Test for the homepage
def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to Power Wash Brothers!" in response.data

# Test for the "About Us" page
def test_about_us(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b"About Us" in response.data

# Test for the FAQ page
def test_faqs(client):
    response = client.get('/faqs')
    assert response.status_code == 200
    assert b"FAQs" in response.data

# Test for the Reviews page
def test_reviews(client):
    response = client.get('/reviews')
    assert response.status_code == 200
    assert b"Reviews" in response.data

# Test for the API route /api/services
def test_list_services(client):
    response = client.get('/api/services')
    assert response.status_code == 200
    assert isinstance(response.json, list)

# Test for the service detail page
def test_service_detail(client):
    response = client.get('/service/1')
    if response.status_code == 200:
        assert b"Description:" in response.data
    else:
        assert response.status_code == 404

# Test for email sending
def test_send_email(mocker):
    mock_send = mocker.patch('flask_mail.Mail.send')

    with flask_app.app_context():  # Using the application context
        send_email('test@example.com', 'Test Subject', '<p>Test Body</p>')

    mock_send.assert_called_once()
    sent_message = mock_send.call_args[0][0]
    assert sent_message.subject == 'Test Subject'
    assert sent_message.recipients == ['test@example.com']
    assert sent_message.html == '<p>Test Body</p>'

# Test for reCAPTCHA verification success
def test_verify_recaptcha_success():
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'success': True}
        token = 'test_token'
        result = verify_recaptcha(token)
        assert result

# Test for reCAPTCHA verification failure
def test_verify_recaptcha_failure():
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'success': False}
        token = 'test_token'
        result = verify_recaptcha(token)
        assert not result

# Test for validation of order form data
def test_validate_order_form_success():
    data = {
        'fullName': 'Test User',
        'email': 'test@example.com',
        'tel': '1234567890',
        'serviceType': 'Test Service',
        'workObjectDetails': 'Test Details'
    }
    is_valid, error_message = validate_order_form(data)
    assert is_valid
    assert error_message == ""

def test_validate_order_form_missing_field():
    data = {
        'fullName': 'Test User',
        'email': 'test@example.com',
        'tel': '1234567890',
        'serviceType': 'Test Service'
    }
    is_valid, error_message = validate_order_form(data)
    assert not is_valid
    assert error_message == "Field workObjectDetails is required."

def test_validate_order_form_invalid_email():
    data = {
        'fullName': 'Test User',
        'email': 'invalid-email',
        'tel': '1234567890',
        'serviceType': 'Test Service',
        'workObjectDetails': 'Test Details'
    }
    is_valid, error_message = validate_order_form(data)
    assert not is_valid
    assert error_message == "Invalid email format."

def test_validate_order_form_invalid_phone():
    data = {
        'fullName': 'Test User',
        'email': 'test@example.com',
        'tel': 'invalid-phone',
        'serviceType': 'Test Service',
        'workObjectDetails': 'Test Details'
    }
    is_valid, error_message = validate_order_form(data)
    assert not is_valid
    assert error_message == "Invalid phone number format."


# Test for order service (need fix)
# def test_order_service(client, mocker):
#     mock_send_email = mocker.patch('app.send_email')
#     mock_save_order = mocker.patch('database.save_order_to_db')
#
#     response = client.post('/service/1/order', data={
#         'fullName': 'Test User',
#         'email': 'test@example.com',
#         'tel': '1234567890',
#         'serviceType': 'Test Service',
#         'workObjectDetails': 'Test Details',
#         'remark': 'Test Remark'
#     })
#
#     assert response.status_code == 302  # checking if the response is a redirect
#     mock_save_order.assert_called_once_with(
#         'Test User', 'test@example.com', '1234567890', 'Test Service', 'Test Details', 'Test Remark'
#     )
#     mock_send_email.assert_any_call(
#         'test@example.com', 'Order Confirmation', user_email_template({
#             'fullName': 'Test User',
#             'email': 'test@example.com',
#             'tel': '1234567890',
#             'serviceType': 'Test Service',
#             'workObjectDetails': 'Test Details',
#             'remark': 'Test Remark'
#         })
#     )
#     mock_send_email.assert_any_call(
#         os.environ.get('ADMIN_EMAIL'), 'New Order Received', admin_email_template({
#             'fullName': 'Test User',
#             'email': 'test@example.com',
#             'tel': '1234567890',
#             'serviceType': 'Test Service',
#             'workObjectDetails': 'Test Details',
#             'remark': 'Test Remark'
#         })
#     )