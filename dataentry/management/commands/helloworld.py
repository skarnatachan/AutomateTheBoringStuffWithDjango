from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Hello World"
    def handle(self, *args, **kwargs):
        # Here, we write the logic
        # self.stdout.write("Hello World")
        print("Hello World")
