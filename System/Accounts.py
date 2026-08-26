from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

class UserNotFoundError(Exception):
    pass
class InvalidPasswordError(Exception):
    pass
class UserAlreadyExistsError(Exception):
    pass

def login(ph: PasswordHasher, account_list: dict, name: str, password: str):
    # Gets the stored password hash from Users.json
    hashed_pw = account_list.get(name)

    # Checks if the user exists
    if hashed_pw is not None:
        try:
            ph.verify(hashed_pw, password)
        except VerifyMismatchError:
            raise InvalidPasswordError()
    else:
        # Raises the exception UserNotFoundError if the user doesn't exist
        raise UserNotFoundError()

def create(ph: PasswordHasher, raw_account_list: dict, name: str, password: str) -> dict:
    account_list = raw_account_list['Users']

    if name not in account_list:
        hashed_pw = ph.hash(password)

        # Adds the new User to account list
        account_list[name] = hashed_pw

        return raw_account_list
    else:
        raise UserAlreadyExistsError()