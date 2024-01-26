from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
def login(request):
    return render(request, "login.html")

@api_view(['GET','POST'])
def testing(request):
    """
    Get information from the API.

    Parameters:
    - `param_name` (string): Your parameter description.

    Response:
    - 200 OK: Successful response.
    """
    user = request.GET.get('user')

    return Response({"hello":user})