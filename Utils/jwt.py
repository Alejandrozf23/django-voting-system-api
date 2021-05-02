import jwt, datetime

def reverseCode(code):
    reverse = ""
    for element in code:
        reverse = element + reverse
    return reverse

class JsonWebToken:    
    @staticmethod
    def generateSecret(access_code, market):
        init = ""
        final = ""
        length = len(access_code)
        for index in range(0, length):
            if (index < market):
                init += access_code[index]
            if (index >= length - market):
                final += access_code[index]
        return reverseCode(final)+access_code+reverseCode(init)

    @staticmethod
    def generateJWT(secret):
        current_time = datetime.datetime.now(datetime.timezone.utc)
        issuedAt = current_time.timestamp()
        expirationTime = issuedAt + (30 * 60)

        payload = {
            'exp':expirationTime,
            'iat':issuedAt
        }

        return jwt.encode(payload, secret, algorithm='HS256')

    @staticmethod
    def validateJWT(jwtoken, secret):
        try:
            jwt.decode(jwtoken, secret, algorithms=["HS256"])
            return {'code':'NE-200','message':'Success'}
        except jwt.ExpiredSignatureError:
            return  {'code':'NE-401','message':'No autorizado. El tiempo de uso del token ha expirado.'}
        except jwt.InvalidSignatureError:
            return  {'code':'NE-401','message':'No autorizado. El token ha sido modificado.'}