from resources.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and user.password==password:
        return user

def identity(payload):
    '''
    Used by JWT to check if a user is already authenticated 
    users send the token in the header which is decoded and 
    returned as payload (stateless)
    '''
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)