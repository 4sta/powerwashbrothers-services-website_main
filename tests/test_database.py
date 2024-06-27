import pytest
from database import get_services_db, get_service_db, get_reviews

# Test for the get_services_db function
def test_get_services_db():
    services = get_services_db()
    assert isinstance(services, list)
    if services:
        assert 'id' in services[0]
        assert 'title' in services[0]

# Test for the get_service_db function
def test_get_service_db():
    service = get_service_db(1)  # Assuming 1 is a valid service ID for the test
    if service:
        assert 'id' in service
        assert 'title' in service
    else:
        assert service is None

# Test for the get_reviews function
def test_get_reviews():
    reviews = get_reviews()
    assert isinstance(reviews, list)
    if reviews:
        assert 'id' in reviews[0]
        assert 'image_url' in reviews[0]