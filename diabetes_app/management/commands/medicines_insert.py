from django.core.management import BaseCommand
from diabetes_app.models import Medicines
from diabetes_app.scraper.medicines_scraper import medicines_scraper


class Command(BaseCommand):
    help = 'Insert initial data into the database'

    def handle(self, *args, **options):
        medicines = medicines_scraper()
        for medicine_data in medicines:
            title = medicine_data['title']
            dose = medicine_data['dose']
            Medicines.objects.create(title=title, dose=dose)

        self.stdout.write(self.style.SUCCESS('Data insertion completed successfully'))
