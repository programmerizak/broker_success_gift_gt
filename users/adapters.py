#To disable email sending during users registaration
# adapters.py
# from allauth.account.adapter import DefaultAccountAdapter

# class NoEmailAccountAdapter(DefaultAccountAdapter):
#     def send_mail(self, template_prefix, email, context):
#         pass

# project/users/adapter.py:
# from django.conf import settings
# from allauth.account.adapter import DefaultAccountAdapter

# class MyAccountAdapter(DefaultAccountAdapter):

#     def get_login_redirect_url(self, request):
#         path = "/accounts/{username}/"
#         return path.format(username=request.user.username)