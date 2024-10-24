from cryptography.fernet import Fernet

# Fernet anahtarı oluşturma
key = Fernet.generate_key()

# Anahtarı byte olarak değil, string formatında yazdırıyoruz
print(key.decode())
