from django.test import TestCase
from django.contrib.auth.models import User
from wiki.models import Page

# Create your tests here.
class WikiTestCase(TestCase):
    def test_true_is_true(self):
        # """  if True is equal to True. Should always pass. '''
        self.assertEqual(True, True)

    def test_page_slugify_on_save(self):
        """ Tests the slug generated when saving a page """
        user = User()
        user.save()

        page = Page(title="Charmander's Bio", content="Charmander, known as Hitokage in Japan, is a Pokémon species in Nintendo's and Game Freak's Pokémon franchise.", author=user)
        page.save()
        #Make sure the slug that was generated in Page.save() matches what we think it should be
        self.assertEqual(page.slug, "charmanders-bio")

class PageListViewTests(TestCase):
    def test_multiple_pages(self):
        # Make some test data to be displayed on the page.
        user = User.objects.create()

        Page.objects.create(title="Test", content="test1", author=user)
        Page.objects.create(title="Another Test", content="test2", author=user)

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        responses = response.context['pages']
        self.assertEqual(len(responses), 2)

        self.assertQuerysetEqual(
            responses,
            ['<Page: Test>', '<Page: Another Test>'],
            ordered=False
        )

        self.assertContains(response, "Test")
        self.assertContains(response, "Another Test")

class PageDetailViewTests(TestCase):
    
    def test_detail_page(self):
        #set up the data
        user = User.objects.create()
        Page.objects.create(title="TestyTest",
            content ="123456789",
            author = user)

        #make a request
        response = self.client.get('/testytest/')

        #check the response
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "TestyTest")
        self.assertContains(response, "123456789")
        self.assertContains(response, user)
