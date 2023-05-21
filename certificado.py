import datetime
from cryptography import x509
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

# Gerando uma chave privada RSA
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Criando um certificado autoassinado
subject = issuer = x509.Name([
    x509.NameAttribute(x509.NameOID.COUNTRY_NAME, 'US'),
    x509.NameAttribute(x509.NameOID.STATE_OR_PROVINCE_NAME, 'California'),
    x509.NameAttribute(x509.NameOID.LOCALITY_NAME, 'San Francisco'),
    x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, 'Example Inc.'),
    x509.NameAttribute(x509.NameOID.COMMON_NAME, 'example.com')
])

cert_builder = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer)
cert_builder = cert_builder.not_valid_before(datetime.datetime.utcnow())
cert_builder = cert_builder.not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
cert_builder = cert_builder.serial_number(x509.random_serial_number())
cert_builder = cert_builder.public_key(private_key.public_key())
cert_builder = cert_builder.add_extension(
    x509.SubjectAlternativeName([x509.DNSName('example.com')]),
    critical=False
)

certificate = cert_builder.sign(private_key, hashes.SHA256(), default_backend())

# Salvando a chave privada em key.pem
with open('key.pem', 'wb') as key_file:
    key_file.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Salvando o certificado em cert.pem
with open('cert.pem', 'wb') as cert_file:
    cert_file.write(certificate.public_bytes(serialization.Encoding.PEM))