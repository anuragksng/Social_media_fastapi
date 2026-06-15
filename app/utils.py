import hashlib
import hmac

def verify(plain_password, hashed_password):

    hash_plain_password = hashlib.sha256(plain_password.encode()).hexdigest()
    return hmac.compare_digest(hash_plain_password, hashed_password)
