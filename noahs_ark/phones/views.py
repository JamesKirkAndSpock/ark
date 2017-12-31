"""Module for phone category and phone views"""
from django.http import Http404
from rest_framework import status, permissions, generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from phones.models import PhoneCategory, Phones
from phones.serializers import PhoneCategorySerializer, PhoneSerializer

# Create your views here.

class PhoneCategoryView(generics.ListCreateAPIView):
    """
    List all phone categories, or create a new phone category.
    """
    queryset = PhoneCategory.objects.all()
    serializer_class = PhoneCategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class PhoneCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a phone category.
    """
    queryset = PhoneCategory.objects.all()
    serializer_class = PhoneCategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PhoneListView(generics.ListCreateAPIView):
    """
    List all phones, in a phone category.
    """
    queryset = Phones.objects.all()
    serializer_class = PhoneSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def check_object(self, pk):
        '''Check that the phone category exists'''
        try:
            PhoneCategory.objects.get(pk=pk)
        except PhoneCategory.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''Retrieve a list of phones in a phone category'''
        self.check_object(pk)
        phone_list = Phones.objects.filter(phone_category=pk)
        serializer = PhoneSerializer(phone_list, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        '''Post a phone in a phone category'''
        self.check_object(pk)
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PhoneDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for a particular phone
    """

    queryset = Phones.objects.filter()
    serializer_class = PhoneSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_object(self, pk2):
        '''Return chosen phone object'''
        try:
            return Phones.objects.get(pk=pk2)
        except Phones.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        '''Retriever phone object data'''
        phone = self.get_object(kwargs['pk2'])
        serializer = PhoneSerializer(phone)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        '''Update phone object data'''
        phone = self.get_object(kwargs['pk2'])
        serializer = PhoneSerializer(phone, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        '''Delete phone object'''
        phone = self.get_object(kwargs['pk2'])
        phone.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def api_root(request, format=None):
    '''View for the root'''
    return Response({
        'Phone-Categories': reverse('phone-category-list', request=request, format=format),
    })
