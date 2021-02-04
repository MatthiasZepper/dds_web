###############################################################################
# IMPORTS ########################################################### IMPORTS #
###############################################################################

# Standard library

# Installed
import flask
import flask_restful

# Own modules
from code_dds.api import user
from code_dds.api import project


###############################################################################
# BLUEPRINTS ##################################################### BLUEPRINTS #
###############################################################################

api_blueprint = flask.Blueprint("api_blueprint", __name__)
api = flask_restful.Api(api_blueprint)


###############################################################################
# RESOURCES ####################################################### RESOURCES #
###############################################################################

# Login/access ################################################# Login/access #
api.add_resource(user.AuthenticateUser, "/user/auth", endpoint="auth")
api.add_resource(project.ProjectAccess,
                 "/proj/auth", endpoint="proj_auth")
