from invenio_pages import InvenioPagesREST
from invenio_pages.rest import blueprint

# mock the rest API url prefix
blueprint.url_prefix = '/api/{}'.format(blueprint.url_prefix)


def test_page_content(pages_fixture):
    """Test page content."""
    app = pages_fixture
    app.register_blueprint(blueprint)

    with app.app_context():
        with app.test_client() as client:
            resp = client.get('/api/pages/1')
            assert resp.status_code == 200
            assert resp.json == {
                'title': 'Page for Dogs!', 'description': '',
                'url': '/dogs', 'content': 'Generic dog.',
                'id': '1', 'links': {
                    'self': 'http://localhost/api/pages/1'
                }
            }


def test_html_content(pages_fixture):
    """Test page content."""
    app = pages_fixture
    app.register_blueprint(blueprint)

    with app.app_context():
        with app.test_client() as client:
            resp = client.get('/api/pages/4')
            assert resp.status_code == 200
            assert resp.json == {
                'title': 'Page for modern dogs!', 'description': '',
                'url': '/htmldog',
                'content': '<h1>HTML aware dog.</h1>.\n'
                           '<p class="test">paragraph<br /></p>',
                'id': '4', 'links': {
                    'self': 'http://localhost/api/pages/4'
                }
            }


def test_page_etag(pages_fixture):
    """Test page content."""
    app = pages_fixture

    app.register_blueprint(blueprint)

    with app.app_context():
        with app.test_client() as client:
            resp = client.get('/api/pages/1')
            assert resp.status_code == 200

            resp = client.get('/api/pages/1',
                              headers=(
                                  ('If-None-Match',
                                   resp.headers.get('ETag')),))
            assert resp.status_code == 304
