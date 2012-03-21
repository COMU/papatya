# Create your views here.
from django.shortcuts import render_to_response

def test(request):

    data = dict()
    data['message'] = "Hello"
    # data = {'message': "Hello", 'messag2':"falan filan"}
    return render_to_response("songs/test.html", data)
