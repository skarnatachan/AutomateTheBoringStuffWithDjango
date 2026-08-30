from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Greets the user"
    def add_arguments(self, parser):
        parser.add_argument("name", type=str, help="The name of the person to greet.")


    def handle(self, *args, **kwargs):
        # Write the logic
        name = kwargs["name"]
        self.stdout.write(f"Good Morning, {name}")
        self.stdout.write(self.style.SUCCESS(f"Good Morning, {name}"))
        self.stdout.write(self.style.WARNING(f"Good Morning, {name}"))
        self.stderr.write(f"Good Morning, {name}")