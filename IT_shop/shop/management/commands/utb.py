from django.core.management import BaseCommand
import webbrowser
class Command(BaseCommand):
	help = 'this is for utube'
	#def add_arguments(self, parser):
	#	parser.add_argument('link', type=str)

	def handle(self,*args, **options):
	#	links = options.get("link")
	#	print (links)
		webbrowser.open('https://www.youtube.com/watch?v=mrTUAxhQ_Uo&list=RDyyLnzcy2Uf8&index=27', new=0)