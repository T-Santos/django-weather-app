"""
Used to gather and auto populate the states data in the database.
"""
# django builtin apps
from django.core.management.base import BaseCommand, CommandError

# local django package
from common.models import State

# util to get state data
from common.utilities.extract.state_dicts import state_name_dict

class Command(BaseCommand):

	help = 'Update States in database'
	requires_system_checks = True

	def handle(self, *args, **options):

		state_code_dict = {v:k for k,v in state_name_dict.items()}

		existing_states_qs = State.objects.all()
		existing_states_dict = {instance.code:instance.name for instance in existing_states_qs}

		for s_code,s_name in state_code_dict.items():
			if s_code not in existing_states_dict:
				State(code=s_code,name=s_name,).save()

		self.stdout.write(self.style.SUCCESS('Successfully updated states.'))