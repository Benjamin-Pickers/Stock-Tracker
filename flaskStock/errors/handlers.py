from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

#custom error routes for 404 and 500 errors
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
