from django.views.debug import technical_500_response
import sys

# Django snippet
# Author: zbyte64
# Posted: July 31, 2008
class UserBasedExceptionMiddleware(object):

    def process_exception(self, request, exception):
        if request.user.is_superuser:
            return technical_500_response(request, *sys.exc_info())
