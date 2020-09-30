from flask import (Blueprint, g, make_response, session, request, jsonify,
                   current_app)
from flask_restful import Resource, Api, reqparse, abort
# from code_dds import db
# from api import my_schema, my_schemas
from code_dds.models import User

from code_dds.marshmallows import user_schema, users_schema
from code_dds.models import S3Project, User, Project

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend


def cloud_access(project):
    '''Gets the S3 project ID (bucket ID).

    Args:
        project:    Specified project ID used in current delivery

    Returns:
        tuple:  access, s3 project ID and error message
    '''

    # Get s3 info if project in database
    s3_info = S3Project.query.filter_by(project_id=project).first()

    # Return error if s3 info not found
    if s3_info is None:
        return False, "", "There is no recorded S3 project for the specified project"

    # Access granted, S3 ID and no error message
    return True, s3_info.id, ""


def ds_access(username, password) -> (bool, int, str):
    '''Finds facility in db and validates the password given by user.

    Args:
        username:   The users username
        password:   The users password

    Returns:
        tuple:  If access to DS granted, facility ID and error message

    '''

    # Get user from database
    fac = User.query.filter_by(username=username).first()

    # Return error if username doesn't exist in database
    if fac is None:
        return False, 0, "The user does not exist"

    # Get password info in response and
    # calculate secure password hash with Scrypt
    sec_pw = secure_password_hash(password_settings=fac.settings,
                                  password_entered=password)

    print(sec_pw, flush=True)
    # Return error if the password doesn't match
    if sec_pw != fac.password:
        return False, 0, "Incorrect password!"

    return True, fac.id, ""


def project_access(uid, project) -> (bool, str):
    '''Checks the users access to the specified project

    Args:
        fac_id:     Facility ID
        project:    Project ID
        owner:      Owner ID

    Returns:
        tuple:  access and error message
    '''

    # Get project info if owner and facility matches
    project_info = Project.query.filter_by(id=project, owner=uid,
                                           facility=uid).first()

    # Return error if project not found
    if project_info is None:
        return False, None, "The project doesn't exist or you don't have access"

    # Return error if project doesn't have access to S3
    if project_info.delivery_option != "S3":
        return False, None, "The project does not have S3 access"

    # Check length of public key and quit if wrong
    # ---- here ----

    return True, project_info.public_key, ""


def secure_password_hash(password_settings: str,
                         password_entered: str) -> (str):
    '''Generates secure password hash.

    Args:
            password_settings:  String containing the salt, length of hash,
                                n-exponential, r and p variables.
                                Taken from database. Separated by '$'.
            password_entered:   The user-specified password.

    Returns:
            str:    The derived hash from the user-specified password.

    '''

    # Split scrypt settings into parts
    settings = password_settings.split("$")
    for i in [1, 2, 3, 4]:
        settings[i] = int(settings[i])  # Set settings as int, not str

    # Create cryptographically secure password hash
    kdf = Scrypt(salt=bytes.fromhex(settings[0]),
                 length=settings[1],
                 n=2**settings[2],
                 r=settings[3],
                 p=settings[4],
                 backend=default_backend())

    return (kdf.derive(password_entered.encode('utf-8'))).hex()


class LoginUser(Resource):
    global DEFAULTS
    DEFAULTS = {
        'access': False,
        'user_id': "",
        's3_id': "",
        'public_key': None,
        'error': ""
    }

    # @marshal_with(login_fields)  # Worked first but stopped working for some
    # reason. Gives response 500.
    def post(self):
        '''Checks the users access to the delivery system.

        Args:
            username:   Username
            password:   Password
            project:    Project ID

        Returns:
            UserInfo with format resource_fields
        '''

        # Get args from request
        user_info = request.args

        # Look for user in database
        ok, uid, error = ds_access(username=user_info['username'],
                                   password=user_info['password'])
        if not ok:  # Access denied
            return jsonify(access=DEFAULTS['access'], user_id=uid,
                           s3_id=DEFAULTS['s3_id'],
                           public_key=DEFAULTS['public_key'],
                           error=error,
                           project_id=user_info['project'])

        # Look for project in database
        ok, public_key, error = project_access(uid=uid,
                                               project=user_info['project'])
        if not ok:  # Access denied
            return jsonify(access=DEFAULTS['access'], user_id=uid,
                           s3_id=DEFAULTS['s3_id'],
                           public_key=DEFAULTS['public_key'],
                           error=error,
                           project_id=user_info['project'])

        # Get S3 project ID for project
        ok, s3_id, error = cloud_access(project=user_info['project'])
        if not ok:  # Access denied
            return jsonify(access=DEFAULTS['access'], user_id=uid,
                           s3_id=s3_id,
                           public_key=DEFAULTS['public_key'],
                           error=error,
                           project_id=user_info['project'])

        # Access approved
        return jsonify(access=True, user_id=uid,
                       s3_id=s3_id,
                       public_key=public_key,
                       error="",
                       project_id=user_info['project'])


class LogoutUser(Resource):
    def get(self):
        return {"class": "LogoutUser", "method": "get"}

    def post(self):
        return {"class": "LogoutUser", "method": "post"}


class ListUsers(Resource):
    def get(self):
        all_users = User.query.all()
        return users_schema.dump(all_users)

    def post(self):
        return {"class": "ListUsers", "method": "post"}
