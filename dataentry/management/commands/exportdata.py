import csv
from datetime import datetime
from django.apps import apps
from django.core.management.base import BaseCommand, CommandError

# proposed command = python manage.py exportdata model_name

class Command(BaseCommand):
    help = "Export data from database to a CSV file"

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help="Model's name")

    def handle(self, *args, **kwargs):
        model_name = kwargs["model_name"]
        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break   # stop executing code once the model is found
            except LookupError:
                continue   # model not found in this app, continue searching in next app.
        if not model:
            raise CommandError(f"Model {model_name} not found in any app!")

        # Fetch the data from database
        data = model.objects.all()

        # Generate the timestamp of current date and time
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        # Define the CSV file name/path
        file_path = f"exported_{model_name}_data_{timestamp}.csv"
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write the CSV header
            # We want to print the field names of the model that we are trying to export
            writer.writerow([field.name for field in model._meta.fields])

            # write data rows
            for dt in data:
                writer.writerow([getattr(dt, field.name) for field in  model._meta.fields])
        self.stdout.write(self.style.SUCCESS("Successfully exported data to CSV file"))


