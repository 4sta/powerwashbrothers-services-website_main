import pytest
from app import app as flask_app

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