import jwt, datetime

current_time = datetime.datetime.now(datetime.timezone.utc)
issuedAt = current_time.timestamp()
expirationTime = issuedAt + (30 * 60)

payload = {
    'exp':expirationTime,
    'iat':issuedAt
}
encoded_jwt = jwt.encode(payload, 'secret', algorithm='HS256')
print(encoded_jwt)

try:
    decode_jwt = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
    print(decode_jwt)
except jwt.ExpiredSignatureError:
    print("TOKEN INVALIDO")
except jwt.InvalidSignatureError:
    print("FIRMA INVALIDA")
