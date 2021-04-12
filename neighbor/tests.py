from django.test import TestCase
from .models import Profile,Neighborhood,Business
from django.contrib.auth.models import User


# Create your tests here.
class ProfileTestClass(TestCase):
    from django.contrib.auth.models import User
    def setUp(self):
        self.user = User(username='martin')
        self.user.save()
        self.profile = Profile(id=1,user=self.user,photo='download.jpeg',bio='My name is Martin', name='person')
        self.profile.save_profile()

    def tearDown(self):
        Profile.objects.all().delete()
        User.objects.all().delete()
        Neighborhood.objects.all().delete()
        Business.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.user,User))
        self.assertTrue(isinstance(self.profile, Profile))

    def test_save_method(self):
        self.profile.save_profile()
        profile = Profile.objects.all()
        self.assertTrue(len(profile) > 0)

class NeighborTestClass(TestCase):
    def setUp(self):
        self.profile = Profile(user=User(username='martin'))
        self.profile.user.save()
        self.profile.save()
        self.post = Neighborhood(id='1',name='Yes', location='Nairobi',
        admin=self.profile,
        hood_logo='default.jpeg', 
        occupants_count='0',
        health_department='0', 
        police_number='0',
        description='this is it',)
        self.post.save_post()

    def test_insatance(self):
        self.assertTrue(isinstance(self.profile,Profile))
        self.assertTrue(isinstance(self.post, Neighborhood))

    def test_create_neigborhood(self):
        self.post.save_post()
        posts = Neighborhood.objects.all()
        self.assertTrue(len(posts) > 0)

    def test_delete_neigborhood(self):
        self.post.save_post()
        self.post.delete_post()
        posts = Neighborhood.objects.all()
        self.assertTrue(len(posts) <= 0)

    def find_neigborhood(self):
        self.post.save_post()
        post = Neighborhood.find_neighborhood(neighborhood_id)
        self.assertEqual(post.id,'1')

    def test_update_neighborhood(self):
        self.post.save_post()
        new_caption =Neighborhood.update_post('this is it','Yeah')
        post = Neighborhood.objects.get(description='Yeah')
        self.assertEqual(post.description,'Yeah')


class BusinessTestClass(TestCase):
    def setUp(self):
        self.profile = Profile(user=User(username='martin'))
        self.profile.user.save()
        self.profile.save()
        self.post = Neighborhood(id='1',name='Yes', location='Nairobi',
        admin=self.profile,
        hood_logo='default.jpeg', 
        occupants_count='0',
        health_department='0', 
        police_number='0',
        description='this is it',)
        self.post.admin.save()
        self.post.save()
        self.business = Business(id='1',name='Yes',
        photo='default.jpeg', 
        email='l@gmsil.com',
        description='this is it',)
        self.business.create_business()

    def test_insatance(self):
        self.assertTrue(isinstance(self.profile,Profile))
        self.assertTrue(isinstance(self.post, Neighborhood))
        self.assertTrue(isinstance(self.business, Business))

    def test_create_neigborhood(self):
        self.business.create_business()
        posts = Business.objects.all()
        self.assertTrue(len(posts) > 0)

    def test_delete_business(self):
        self.business.create_business()
        self.business.delete_business()
        posts = Business.objects.all()
        self.assertTrue(len(posts) <= 0)

    def find_business(self):
        self.business.create_business()
        post = Business.find_business(business_id)
        self.assertEqual(post.id,'1')

#     def test_update_business(self):
#         self.business.create_business()
#         new_caption =Business.update_post('this is it','Yeah')
#         post = Business.objects.get(description='Yeah')
#         self.assertEqual(post.description,'Yeah')