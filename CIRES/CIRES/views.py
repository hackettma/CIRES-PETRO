from django.http import Http404, HttpResponse
import datetime

def hello(request):
	return HttpResponse("Hello world!")

def time(request):
	now = datetime.datetime.now()
	html = '<html><body>The time is %s</body></html>' %now
	return HttpResponse(html)

def time_offset(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()

	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	html = '<html><body>In %s hours, the time will be %s </body></html>' %(offset, dt)
	return HttpResponse(html)