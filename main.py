from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware
from app.resources import app as critique
# from forum_admin.application import app as forum_admin

application = DispatcherMiddleware(critique)
if __name__ == '__main__':
    run_simple('localhost', 5000, application,
               use_reloader=True, use_debugger=True, use_evalex=True)
