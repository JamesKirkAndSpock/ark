'''Module to serialize input for models'''
from rest_framework import serializers
from phones.models import PhoneCategory, Phones

class PhoneCategorySerializer(serializers.ModelSerializer):
    '''Class serializer for Phone Category Serializers'''
    name = serializers.CharField(label='Phone Category Name',
                                 required=True,
                                 allow_blank=False,
                                 max_length=15,
                                )

    class Meta:
        '''Define fields for phone categories'''
        model = PhoneCategory
        fields = ('name', 'id')


class PhoneSerializer(serializers.ModelSerializer):
    '''Class Serializer for Phone Objects'''
    phone_name = serializers.CharField(label='Phone Name',
                                       required=True,
                                       allow_blank=False, max_length=15
                                      )
    price = serializers.IntegerField(label="Shs.", max_value=250000, min_value=0)

    class Meta:
        '''Define fields to be used for Phones'''
        model = Phones
        fields = ('phone_name', 'id', 'phone_category', 'price', 'photo',
                  'details', 'front_image', 'side_image', 'back_image')
