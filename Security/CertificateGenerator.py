from cryptography.hazmat.primitives import serialization
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
import datetime
from RSAKeyGenerator import RSAKeyGenerator

class CertificateGenerator(RSAKeyGenerator):
    def __init__(self) -> None:
        super().__init__()
        
    def generateCSR(self):
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "IL"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Haifa"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Ramla"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Orel6505"),
            x509.NameAttribute(NameOID.COMMON_NAME, "Orel Yosupov"),
        ])
        
        cert = x509.CertificateBuilder()
        cert = cert.subject_name(subject)
        cert = cert.issuer_name(issuer)
        cert = cert.public_key(self.key.public_key())
        cert = cert.serial_number(x509.random_serial_number())
        cert = cert.not_valid_before(datetime.datetime.now(datetime.timezone.utc))
        cert = cert.not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=10))
        cert = cert.sign(self.key, hashes.SHA256())
        
        CertificateGenerator.writeToSafe(cert.public_bytes(serialization.Encoding.PEM), "certification")
        
    def checkCSR(key: bytes):
        temp = x509.load_pem_x509_certificate(key)
        if datetime.datetime.timestamp(temp.not_valid_after_utc) < datetime.datetime.timestamp(datetime.datetime.now()): return False
        return True