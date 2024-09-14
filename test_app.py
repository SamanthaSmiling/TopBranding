import pytest
from brand_glimpse import read_file, glimpse

@pytest.fixture
def client():
    read_file.config['data/transaction_data.csv'] = True
    with read_file.test_client() as client:
        yield client

def test_home(client):
    rv = client.get('/')
    assert rv.status_code == 200
