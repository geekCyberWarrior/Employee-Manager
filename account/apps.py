from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'account'

    # THE BELOW METHOD IS OVERRIDEN INORDER FOR THE SIGNALS TO WORK FINE
    def ready(self):
    	import account.signals