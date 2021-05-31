from apiproject import bcrypt

def generate_password(password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    return hashed_password

def validate_password(pw_hash, pw_candidate):
    return bcrypt.check_password_hash(pw_hash, pw_candidate)