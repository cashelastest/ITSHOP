from django.core.exceptions import ValidationError
from django.utils.translation import gettext


class PasswordValidator:
	def __init__(self, sponsor = '_Mr_Rac_'):
		self.sponsor = sponsor
	def validate(self, password, user = None):
		if self.sponsor.lower() not in password.lower():
			raise ValidationError(
				gettext(f'''Мррр-р, котик каже, що у вашому паролі має міститися ім'я спонсора{self.sponsor}''')
				)

	def get_help_text(self):
		return '''Пароль має містити ім'я спонсора'''