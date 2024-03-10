import datetime
from RSAKeyManager import RSAKeyManager

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization

# Class to manage Certificate Singing Request (CSR), It inherits from RSAKeyManager Because it creates key to self sign
class CertificateManager(RSAKeyManager):
    
    #Creates RSA Key for the certification generation
    def __init__(self) -> None:
        super().__init__()
    
    # Generate self signed CSR certificate
    @classmethod
    def GenerateCertificate(key: RSAKeyManager, Country: str, Province: str, Locality: str, OrgName: str, CommonName: str, ExpireIn: int=10) -> x509.Certificate:
        # Creates the issuer and subject object which contains all the required data
        # Country name - Your country name in Two-letter code (ISO 3166)
        #
        #
        # Common name - Your full name
        # Organization name	- Your username or the organization’s name
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, Country),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, Province),
            x509.NameAttribute(NameOID.LOCALITY_NAME, Locality),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, OrgName),
            x509.NameAttribute(NameOID.COMMON_NAME,CommonName),
        ])
        
        # Takes the current datetime
        DateNow: datetime = datetime.datetime.now(datetime.timezone.utc)
        
        # Create Certificate object builder
        cert = x509.CertificateBuilder()
        # Apply the required data
        cert = cert.subject_name(subject)
        cert = cert.issuer_name(issuer)
        
        # Insert the generated public key
        cert = cert.public_key(key.privKey.public_key())
        
        # Generate unique serial number
        # Every serial number is unique to each certificate
        cert = cert.serial_number(x509.random_serial_number())
        
        # Set the expiration date of this certificate
        cert = cert.not_valid_before(DateNow)
        cert = cert.not_valid_after(DateNow + datetime.timedelta(days=ExpireIn))
        
        # Sign this key with the generated private key
        cert = cert.sign(key.privKey, hashes.SHA256())
        return cert
    
    # Tries to Load the certificate
    @staticmethod
    def WriteCertToSafe(cert: x509.Certificate, FilePath: str, FileName: str):
        RSAKeyManager.writeToSafe(cert.public_bytes(serialization.Encoding.PEM), FilePath, FileName)
        
    # Tries to Load the certificate
    @staticmethod
    def ReadCertificateFromSafe(FilePath: str, FileName: str) -> bytes:
        return RSAKeyManager.readFromSafe(FilePath, FileName)
    