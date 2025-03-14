from django.middleware.csrf import rotate_token
from django.utils.crypto import salted_hmac, constant_time_compare
from django.contrib.auth.hashers import check_password, make_password
from django.conf import settings
from .models import UserRegister


def user_authenticate(request, email, password):
    """
    Function that checks if an user can be authenticated to the system
    :param email:
    :param password:
    :return:
    """
    try:
        user = UserRegister.objects.get(email=email, password=password)
    except UserRegister.DoesNotExist:
        return None
    else:
        return user
        
def user_login(request, user):
    """
     We log in an user on the extranet
    :param request:
    :param user:
    :return:
    """
    session_user_auth_hash = calculate_user_session_hash(user.password)
    if "USER_SESSION_ID" in request.session:
        if get_user_session_id(request) != user.id or not constant_time_compare(request.session.get("USER_SESSION_HASH", ''), session_user_auth_hash):
            request.session.flush()
            try:
                del request.session['USER_SESSION_ID']
                del request.session['USER_SESSION_HASH']
                del request.session["USER_ACCOUNT_TYPE"]
            except KeyError:
                pass
    else:
        request.session.cycle_key()

    request.session["USER_SESSION_ID"] = user.id
    request.session["USER_SESSION_HASH"] = session_user_auth_hash
    rotate_token(request)


def user_logout(request):
    """
    :param request:
    :return:
    """
    try:
        del request.session['USER_SESSION_ID']
        del request.session['USER_SESSION_HASH']
    except KeyError:
        pass


def get_user_session_id(request):
    """
     We get the session id of the user if logged in
    :param request:
    :return:
    """
    if "USER_SESSION_ID" in request.session:
        return request.session.get("USER_SESSION_ID", None)
    else:
        return None


def get_user_session_hash(request):
    """
     We get the session id of the user if logged in
    :param request:
    :return:
    """
    if "USER_SESSION_HASH" in request.session:
        return request.session.get("USER_SESSION_HASH", None)
    else:
        return None


def calculate_user_session_hash(value):
    """
     We get the session id of the user if logged in
    :param value:
    :return:
    """
    key_salt = "e_commerce_apps.accounts.auth.get_user_session_hash"
    return salted_hmac(key_salt, value).hexdigest()

def user_is_authenticated(request):
    """
     We check if the user is authenticated
    :param request:
    :return:
    """
    user_session_id = get_user_session_id(request)
    user_session_hash = get_user_session_hash(request)
    try:
        user = UserRegister.objects.get(id=user_session_id, is_active=True)
    except UserRegister.DoesNotExist:
        return False
    if constant_time_compare(user_session_hash, calculate_user_session_hash(user.password)):
        return user
    else:
        return False
