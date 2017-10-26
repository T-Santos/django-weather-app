from django.core.management.base import BaseCommand, CommandError

from common.models import SignupLocation, State

# util to get location data from api
from common.utilities.extract.extract_locations import extract_locations

class Command(BaseCommand):

    help = 'Updates the location values in database'
    requires_system_checks = True
    requires_migrations_checks = True

    def handle(self, *args, **options):

        existing_states_qs = State.objects.all()
        if not existing_states_qs:
            error = "No states found. Please run the 'manage.py update_states' command first."
            self.stdout.write(
                self.style.ERROR(error))
        else:
            new_locations = extract_locations(top_N=100)
            existing_states_dict = {instance.code:instance for instance in existing_states_qs}
            
            for new_city,_,new_state_code in new_locations:

                if new_state_code not in existing_states_dict:
                    error = 'An error was encountered. Attmpting to add location with non existing state.'
                    self.stdout.write(
                        self.style.ERROR(error))
                elif SignupLocation.objects.filter(city=new_city,state__code=new_state_code):
                    # already in database
                    pass
                else:
                    new_location = SignupLocation(city=new_city,state=existing_states_dict[new_state_code])
                    new_location.save()

            # report successful update
            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully updated locations.'))