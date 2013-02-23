from google.appengine.api import users
import logging
import sys
import traceback

class UserService(object):

    def create_login_url(self, dest_url):
        try:
            return users.create_login_url(dest_url)
        except Exception, e:
            self._print_stack_trace()
            raise e

    def create_logout_url(self, dest_url):
        try:
            return users.create_logout_url(dest_url)
        except Exception, e:
            self._print_stack_trace()
            raise e

    def get_current_user(self):
        try:
            return users.get_current_user()
        except Exception, e:
            self._print_stack_trace()
            raise e

    def is_current_user_admin(self):
        try:
            return users.is_current_user_admin()
        except Exception, e:
            self._print_stack_trace()
            raise e

    def _print_stack_trace(self):
        logging.error(''.join(traceback.format_exception(*sys.exc_info())))
