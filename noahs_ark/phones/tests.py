'''Test file for the phone app'''
import json
from django.test import TestCase
from django.contrib.auth.models import User
from phones.models import PhoneCategory, Phones
from phones.serializers import PhoneCategorySerializer, PhoneSerializer

class PhoneCategoryTestCase(TestCase):
    '''
    Test Serialization and Models for the phone category object
    '''

    def test_phone_categories_created(self):
        '''Test that a phone category is created and added to the model'''
        PhoneCategory.objects.create(name="Samsung")
        self.assertEqual(PhoneCategory.objects.count(), 1)

    def test_phone_categories_updated(self):
        '''Test that a phone category can be updated'''
        PhoneCategory.objects.create(name="Samsung")
        self.assertEqual(PhoneCategory.objects.get(pk=1).name, "Samsung")
        phone_object = PhoneCategory.objects.get(pk=1)
        phone_object.name = "Iphone"
        phone_object.save()
        self.assertEqual(PhoneCategory.objects.get(pk=1).name, "Iphone")

    def test_phone_categories_deleted(self):
        '''Test that a phone category can be deleted'''
        PhoneCategory.objects.create(name="Samsung")
        self.assertEqual(PhoneCategory.objects.count(), 1)
        phone_object_1 = PhoneCategory.objects.get(pk=1)
        phone_object_1.delete()
        self.assertEqual(PhoneCategory.objects.count(), 0)


    def test_serialized_name_valid(self):
        '''Test that the name of the phone object is valid'''
        serialized_phone_object_0 = PhoneCategorySerializer(data={'name':'Samsung'})
        self.assertEqual(serialized_phone_object_0.is_valid(), True)


    def test_name_not_blank(self):
        '''Test that the name added on the serializer is not blank'''
        serialized_phone_object_1 = PhoneCategorySerializer(data={'name':''})
        self.assertEqual(serialized_phone_object_1.is_valid(), False)

    def test_name_not_large(self):
        '''Test that the name of the serializer cannot be greate than 15
        characters
        '''
        dummy_data = {'name': 'examplewithgreaterthanfifteenchar'}
        serialized_phone_object_2 = PhoneCategorySerializer(data=dummy_data)
        self.assertEqual(serialized_phone_object_2.is_valid(), False)

class PhoneTestCase(TestCase):
    '''
    Test Serialization and Models for the phone object
    '''

    def setUp(self):
        self.phone_category = PhoneCategory.objects.create(name="Samsung")

    def test_phone_creation(self):
        '''Test that the phone is created and added to the model'''
        Phones.objects.create(phone_name="Samsung S7",
                              phone_category=self.phone_category,
                              price=20000)
        self.assertEqual(Phones.objects.count(), 1)

    def test_phone_delete(self):
        '''Test that the phone is created and deleted to the model'''
        phones_object = Phones.objects.create(phone_name="Samsung S7",
                                              phone_category=self.phone_category)
        phones_object.delete()
        self.assertEqual(Phones.objects.count(), 0)

    def test_phone_update(self):
        '''Test that the phone is updated'''
        phones_object_1 = Phones.objects.create(phone_name="Samsung S7",
                                                phone_category=self.phone_category)
        self.assertEqual(phones_object_1.phone_name, "Samsung S7")
        phones_object_1.phone_name = "Samsung S6"
        phones_object_1.save()
        self.assertEqual(phones_object_1.phone_name, "Samsung S6")

    def test_serialized_phone_valid(self):
        '''Test that the phone can be created'''
        serialized_phone_0 = PhoneSerializer(data={'phone_name':'Samsung S7',
                                                   'phone_category':self.phone_category.pk,
                                                   'price': 20000
                                                  }
                                            )
        self.assertEqual(serialized_phone_0.is_valid(), True)

    def test_phonename_not_blank(self):
        '''Test that the phone name can't be blank'''
        phone_object_2 = PhoneSerializer(data={'phone_name':'',
                                               'phone_category':self.phone_category.pk,
                                               'price': 20000
                                              }
                                        )
        self.assertEqual(phone_object_2.is_valid(), False)
        self.assertEqual(len(phone_object_2.errors), 1)
        self.assertEqual(phone_object_2.errors['phone_name'], ['This field may not be blank.'])

    def test_phonename_not_large(self):
        '''Test that the phone name is not large'''
        dummy_data_2 = {'phone_name': 'examplewithgreaterthanfifteenchar',
                        'phone_category':self.phone_category.pk,
                        'price': 20000
                       }
        phone_object_3 = PhoneSerializer(data=dummy_data_2)
        self.assertEqual(phone_object_3.is_valid(), False)
        self.assertEqual(len(phone_object_3.errors), 1)
        self.assertEqual(phone_object_3.errors['phone_name'],
                         ['Ensure this field has no more than 15 characters.'])

    def test_price_not_large(self):
        '''Test that the phone name is not larger than 250000'''
        dummy_data_3 = {'phone_name': 'example',
                        'price': 250001,
                        'phone_category':self.phone_category.pk
                       }
        phone_object_4 = PhoneSerializer(data=dummy_data_3)
        self.assertEqual(phone_object_4.is_valid(), False)
        self.assertEqual(len(phone_object_4.errors), 1)
        self.assertEqual(phone_object_4.errors['price'],
                         ['Ensure this value is less than or equal to 250000.'])

    def test_price_not_negative(self):
        '''Test that the phone name is not lower than 0'''
        dummy_data_4 = {'phone_name': 'example',
                        'price': -1,
                        'phone_category':self.phone_category.pk
                       }
        phone_object_5 = PhoneSerializer(data=dummy_data_4)
        self.assertEqual(phone_object_5.is_valid(), False)
        self.assertEqual(len(phone_object_5.errors), 1)
        self.assertEqual(phone_object_5.errors['price'],
                         ['Ensure this value is greater than or equal to 0.'])

class PhoneViewTestCase(TestCase):
    '''
    Test the views and url paths for phone categories and phones
    '''
    def setUp(self):
        '''Creating a user who logins for testing'''
        self.alice = User(username="alice", email="alice@example.org")
        self.alice.set_password("password")
        self.alice.save()

    def test_phone_category_view_get(self):
        '''Test that the phone category is returned on the url for both a
        complete and a detail list
        '''
        PhoneCategory.objects.create(name="Samsung")
        category_view = self.client.get("/category/")
        self.assertContains(category_view, "Samsung")
        category_view_detail = self.client.get("/category/1/")
        self.assertContains(category_view_detail, "Samsung")

    def test_phone_category_update(self):
        '''Test for an update of a phone category'''
        self.client.login(username="alice", password="password")
        PhoneCategory.objects.create(name="Pia")
        data = dict(name="Paa")
        category_update = self.client.put("/category/1/",
                                          data=json.dumps(data),
                                          content_type='application/json')
        self.assertEqual(category_update.status_code, 200)
        response = self.client.get("/category/1/")
        self.assertContains(response, "Paa")
        self.assertEqual(PhoneCategory.objects.get(pk=1).name, "Paa")

    def test_phone_category_delete(self):
        '''Test that a phone category can be deleted by a logged in user'''
        self.client.login(username="alice", password="password")
        PhoneCategory.objects.create(name="Pia")
        get_response = self.client.get("/category/1/")
        self.assertContains(get_response, "Pia")
        delete_response = self.client.delete("/category/1/")
        self.assertEqual(delete_response.status_code, 204)
        get_response = self.client.get("/category/1/")
        self.assertEqual(get_response.status_code, 404)

    def test_phone_category_not_exist(self):
        '''Test that a phone category does note exist returns a 404'''
        response = self.client.get("/category/1/")
        self.assertEqual(response.status_code, 404)

    def test_phone_category_view_post(self):
        '''Test that the phone category is posted and retrieved
        '''
        self.client.login(username="alice", password="password")
        category_view_2 = self.client.post("/category/", {'name': 'example'})
        self.assertEqual(category_view_2.status_code, 201)
        category_view_1_detail = self.client.get("/category/1/")
        self.assertContains(category_view_1_detail, "example")

    def test_all_phones(self):
        '''Test the retrieval of phones under different phone categories'''
        phone_category = PhoneCategory.objects.create(name="Samsung")
        phone_category_1 = PhoneCategory.objects.create(name="Iphone")
        Phones.objects.create(phone_name="Samsung S7",
                              phone_category=phone_category)
        Phones.objects.create(phone_name="Iphone 7",
                              phone_category=phone_category_1)
        phone_view = self.client.get("/category/1/phones/")
        self.assertContains(phone_view, "Samsung S7")
        self.assertNotContains(phone_view, "Iphone 7")
        phone_view_2 = self.client.get("/category/2/phones/")
        self.assertContains(phone_view_2, "Iphone 7")
        self.assertNotContains(phone_view_2, "Samsung S7")


    def test_phone_inexsistent_category(self):
        '''Test that a phone category does not exist'''
        response = self.client.get("/category/1/phones/")
        self.assertEqual(response.status_code, 404)

    def test_phone_post(self):
        '''Test that a phone can be posted under a phone category'''
        self.client.login(username="alice", password="password")
        phone_category = PhoneCategory.objects.create(name="Samsung")
        phone_category_2 = PhoneCategory.objects.create(name="Iphone")
        get_response = self.client.get("/category/1/")
        get_response_2 = self.client.get("/category/2/")
        self.assertEqual(get_response_2.status_code, 200)
        self.assertEqual(get_response.status_code, 200)
        phone_post = self.client.post("/category/1/phones/",
                                      {'phone_name': 'Samsung S7',
                                       'phone_category': phone_category.pk,
                                       'price': 10000
                                      }
                                     )
        phone_post_1 = self.client.post("/category/2/phones/",
                                        {'phone_name': 'Iphone 7',
                                         'phone_category': phone_category_2.pk,
                                         'price': 20000
                                        }
                                       )
        self.assertEqual(phone_post.status_code, 201)
        self.assertEqual(phone_post_1.status_code, 201)
        phone_get = self.client.get("/category/1/phones/")
        self.assertContains(phone_get, "Samsung S7")
        self.assertNotContains(phone_get, "Iphone 7")
        phone_get_2 = self.client.get("/category/2/phones/")
        self.assertContains(phone_get_2, "Iphone 7")
        self.assertNotContains(phone_get_2, "Samsung S7")

    def test_phone_not_exist(self):
        '''Test a 404 not found if a phone does not exist'''
        phone_get = self.client.get("/category/1/phones/1/")
        self.assertEqual(phone_get.status_code, 404)

    def test_phone_get(self):
        '''Test that a phone is retrieved'''
        self.client.login(username="alice", password="password")
        phone_category = PhoneCategory.objects.create(name="Samsung")
        phone_post = self.client.post("/category/1/phones/",
                                      {'phone_name': 'Samsung S7',
                                       'phone_category': phone_category.pk,
                                       'price': 20000
                                      }
                                     )
        self.assertEqual(phone_post.status_code, 201)
        phone_get = self.client.get("/category/1/phones/1/")
        self.assertContains(phone_get, "Samsung S7")

    def test_phone_put(self):
        '''Test that a phone is updated'''
        self.client.login(username="alice", password="password")
        phone_category = PhoneCategory.objects.create(name="Pia")
        Phones.objects.create(phone_name="example1", phone_category=phone_category)
        data = dict(phone_name="example2", phone_category=phone_category.pk, price=20000)
        phone_name_update = self.client.put("/category/1/phones/1/",
                                            data=json.dumps(data),
                                            content_type='application/json')
        self.assertEqual(phone_name_update.status_code, 200)
        response = self.client.get("/category/1/phones/1/")
        self.assertContains(response, "example2")
        self.assertEqual(Phones.objects.get(pk=1).phone_name, "example2")

    def test_phone_delete(self):
        '''Test that a phone is deleted'''
        self.client.login(username="alice", password="password")
        phone_category = PhoneCategory.objects.create(name="Pia")
        Phones.objects.create(phone_name="example1", phone_category=phone_category)
        self.assertEqual(Phones.objects.count(), 1)
        phone_delete = self.client.delete("/category/1/phones/1/")
        self.assertEqual(phone_delete.status_code, 204)
        self.assertEqual(Phones.objects.count(), 0)

    def test_phonecategory_permission(self):
        '''Test that a phone category is created only with permission'''
        category_view_3 = self.client.post("/category/", {'name': 'example'})
        self.assertEqual(category_view_3.status_code, 403)

    def test_permission_phonecategory(self):
        '''
        Test that a phone category is updated or deleted only with
        permission
        '''
        PhoneCategory.objects.create(name="Pia")
        data = dict(name="Paa")
        category_update = self.client.put("/category/1/",
                                          data=json.dumps(data),
                                          content_type='application/json')
        self.assertEqual(category_update.status_code, 403)
        delete_response = self.client.delete("/category/1/")
        self.assertEqual(delete_response.status_code, 403)

    def test_phone_create_permission(self):
        '''Test that a phone is created only with permission'''
        phone_category = PhoneCategory.objects.create(name="Samsung")
        phone_post = self.client.post("/category/1/phones/",
                                      {'phone_name': 'Samsung S7',
                                       'phone_category': phone_category.pk
                                      })
        self.assertEqual(phone_post.status_code, 403)

    def test_permission_phones(self):
        '''
        Test that a phone is updated or deleted only with
        permission
        '''
        phone_category = PhoneCategory.objects.create(name="Pia")
        Phones.objects.create(phone_name="example1", phone_category=phone_category)
        data = dict(phone_name="example2", phone_category=phone_category.pk)
        phone_name_update = self.client.put("/category/1/phones/1/",
                                            data=json.dumps(data),
                                            content_type='application/json')
        self.assertEqual(phone_name_update.status_code, 403)
        phone_delete = self.client.delete("/category/1/phones/1/")
        self.assertEqual(phone_delete.status_code, 403)
