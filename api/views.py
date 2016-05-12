from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser

# Create your views here.
class FetchGallery(APIView):
    parser_classes = (FileUploadParser,)

    def put (self,request, filename, format=None):
        file_obj = request.data['file']

        return Response(status=204)
