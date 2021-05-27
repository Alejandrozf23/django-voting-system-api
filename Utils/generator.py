import random, string, secrets

def getPosition(lenght):
        return random.randint(0, lenght-1)

class GeneratorPassword:
    @staticmethod
    def generateKey(length):
        sizeUpper = 0
        sizeLower = 0
        sizeDigit = 0
        password_array = ['' for i in range(length)]
        size = length / 3
        modulo =  length % 3
        if modulo == 0:
            sizeUpper = sizeLower = sizeDigit = size
        else:
            if modulo == 1:
                sizeUpper = size + 1
                sizeLower = sizeDigit = size
            elif modulo == 2:
                sizeUpper = sizeLower = size + 1
                sizeDigit = size

        upper = ''.join(secrets.choice(string.ascii_uppercase) for i in range(int(sizeUpper)))
        lower = ''.join(secrets.choice(string.ascii_lowercase) for x in range(int(sizeLower)))
        digit = ''.join(secrets.choice(string.digits) for x in range(int(sizeDigit)))
        
        for i in range(len(upper)):
            position = random.randint(0, length-1)
            while password_array[position] != '':
                position = random.randint(0, length-1)
            password_array[position] = upper[i]
        
        for i in range(len(lower)):
            position = random.randint(0, length-1)
            while password_array[position] != '':
                position = random.randint(0, length-1)
            password_array[position] = lower[i]

        for i in range(len(digit)):
            position = random.randint(0, length-1)
            while password_array[position] != '':
                position = random.randint(0, length-1)
            password_array[position] = digit[i]

        password = ''
        for i in range(len(password_array)):
            password += password_array[i]

        return password