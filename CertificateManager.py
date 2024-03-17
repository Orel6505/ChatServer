import datetime
from CryptoHelper import CryptoHelper

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization

# Class to manage Certificate Singing Request (CSR), It inherits from RSAKeyManager Because it creates key to self sign
class CertificateManager():
    
    trustedIssuers = ["Trusted CA Inc", "SecureSign RootCA11", "Orel Yosupov"]
    trustedClients = ["Trusted CA Inc", "SecureSign RootCA11", "Orel Yosupov"]

    # Generate self signed CSR certificate
    @staticmethod
    def GenerateCertificate(privKey, pubKey, Country: str, Province: str, Locality: str, OrgName: str, CommonName: str, ExpireIn: int=10) -> x509.Certificate:
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
            x509.NameAttribute(NameOID.COMMON_NAME, CommonName),
        ])
        
        # Takes the current datetime
        DateNow: datetime = datetime.datetime.now(datetime.timezone.utc)
        
        # Create Certificate object builder
        cert = x509.CertificateBuilder()
        # Apply the required data
        cert = cert.subject_name(subject)
        cert = cert.issuer_name(issuer)
        
        # Insert the generated public key
        cert = cert.public_key(pubKey)
        
        # Generate unique serial number
        # Every serial number is unique to each certificate
        cert = cert.serial_number(x509.random_serial_number())
        
        # Set the expiration date of this certificate
        cert = cert.not_valid_before(DateNow)
        cert = cert.not_valid_after(DateNow + datetime.timedelta(days=ExpireIn))
        
        # Sign this key with the generated private key
        cert = cert.sign(privKey, hashes.SHA256())
        return cert
    
    @staticmethod
    def WriteCertToSafe(self, Key: bytes, SafeLocation:str, FileName: str):
        with open(f'{SafeLocation}/{FileName}.pem', "wb") as f:
            f.write(Key)
    
    @staticmethod
    def ReadCertificateFromSafe(self, SafeLocation:str, FileName: str):
        with open(f'{SafeLocation}/{FileName}.pem', "rb") as f:
            return f.read()
    
    @staticmethod
    def LoadCertificate(cert: bytes):
        return x509.load_pem_x509_certificate(cert, default_backend())
    
    @staticmethod
    def ValidateCertificate(cert: x509.Certificate, TrustedList: list):
        
        # Check the certificate's validity period
        currentTime = datetime.datetime.utcnow()
        if currentTime < cert.not_valid_before or currentTime > cert.not_valid_after:
            return False
                
        # Check if the issuer is in the list of trusted issuers
        issuer = cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
        if issuer not in TrustedList:
            return False
        
        return True
    
    @staticmethod
    def ValidateCertificate(cert: x509.Certificate, TrustedList: list):
        
        # Check the certificate's validity period
        currentTime = datetime.datetime.utcnow()
        if currentTime < cert.not_valid_before or currentTime > cert.not_valid_after:
            return False
                
        # Check if the issuer is in the list of trusted issuers
        issuer = cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
        if issuer not in TrustedList:
            return False
        
        return True
    
    @staticmethod
    def ValidateCertificate(cert: x509.Certificate, TrustedList: list=trustedIssuers):
        # Check the certificate's validity period
        currentTime = datetime.datetime.utcnow()
        if currentTime < cert.not_valid_before or currentTime > cert.not_valid_after:
            return False
        
        # Check if the issuer is in the list of trusted issuers
        issuer = cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
        if issuer not in TrustedList:
            return False
        
        return True
    
    @staticmethod
    def ValidateCSR(cert: x509.Certificate, TrustedList: list=trustedClients):
        # Check the certificate's validity period
        currentTime = datetime.datetime.utcnow()
        if currentTime < cert.not_valid_before or currentTime > cert.not_valid_after:
            return False
        
        # Check if the issuer is in the list of trusted issuers
        issuer = cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
        if issuer not in TrustedList:
            return False
        
        return True