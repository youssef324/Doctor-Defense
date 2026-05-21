import os
from app import create_app
import ssl

app = create_app()

if __name__ == '__main__':
    use_https = os.environ.get('USE_HTTPS', '').lower() in ('1', 'true', 'yes')

    scheme = 'https' if use_https else 'http'
    ssl_context = None

    if use_https:
        pfx_file = 'cert.pfx'  # Change if you used different name/path
        pfx_password = '123456'  # Same password you used above

        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_pkcs12(open(pfx_file, 'rb').read(), password=pfx_password.encode())

    print()
    print('🚀 Secure Document Vault is starting...')
    print(f'🔗 Open in your browser: {scheme}://127.0.0.1:5000')
    if use_https:
        print('⚠️  Using self-signed certificate (browser may show warning)')
    print('⏹️  Press Ctrl+C to stop')
    print()

    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True,
        use_reloader=False,
        ssl_context='adhoc'
    )