import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import app

def handler(event, context):
    """Handler de Netlify Functions"""
    from werkzeug.wrappers import Request, Response
    
    # Crear request desde el event de Netlify
    environ = {
        'REQUEST_METHOD': event.get('httpMethod', 'GET'),
        'PATH_INFO': event.get('path', '/'),
        'QUERY_STRING': event.get('queryStringParameters', ''),
        'CONTENT_TYPE': event.get('headers', {}).get('content-type', ''),
        'CONTENT_LENGTH': len(event.get('body', '')),
        'wsgi.input': event.get('body', ''),
        'wsgi.url_scheme': 'https',
        'SERVER_NAME': 'localhost',
        'SERVER_PORT': '443',
    }
    
    # Agregar headers
    for key, value in event.get('headers', {}).items():
        key = key.upper().replace('-', '_')
        environ[f'HTTP_{key}'] = value
    
    # Ejecutar la app Flask
    with app.request_context(environ):
        response = app.full_dispatch_request()
        
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.get_data(as_text=True)
        }
