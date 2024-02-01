from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ServerSSLCertificate
from .ssl_service import get_ssl_certificate_details

# Create your views here.
def login(request):
    return render(request, "login.html")


@api_view(["POST"])
def add_server(request):
    requried_fields = ["name", "domain"]
    for field in requried_fields:
        if not request.data.get(field, None):
            return Response(data={"error": "INVALID_ENTRY", "error_message":f"{field} is required"}, status=status.HTTP_417_EXPECTATION_FAILED,exception=True)
        
    new_server_record = ServerSSLCertificate(
        server_name=request.data.get("name"),
        url=request.data.get("domain")
    )
    new_server_record.save()
    get_ssl_certificate_details(request.data.get("domain"))
    return Response({"server": new_server_record.to_dict()},status=status.HTTP_201_CREATED)


@api_view(['POST'])
def force_sync(request):
    if not request.data.get("domain", None):
        return Response(data={"error": "INVALID_ENTRY", "error_message":f"domain is required"}, status=status.HTTP_417_EXPECTATION_FAILED, exception=True)
    updated_servers = get_ssl_certificate_details(request.data.get("domain"))
    return Response({"servers":updated_servers,"count": len(updated_servers)})


@api_view(['GET'])
def get_servers(request):
    """
    List servers available in database.

    Parameters:

    Response:
    - 200 OK: Successful response.
    """
    # user = request.GET.get('user')
    servers = ServerSSLCertificate.objects.all()

    return Response({"servers":[server.to_dict() for server in servers],"count": len(servers)})