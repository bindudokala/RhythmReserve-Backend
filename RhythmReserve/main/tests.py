from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponse

class MainViewsTestCase(TestCase):
    def test_index_view(self):
        # Test the index view
        url = reverse('index')  # Assuming you have a URL pattern with the name 'index'
        response = self.client.get(url)

        # Check that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the content of the response matches the expected text
        self.assertEqual(response.content.decode('utf-8'), "Hello, world. You're at the main index.")


    def run_all_tests(self):
        # Run the test method
        self.test_index_view()

        # Print a statement indicating that all tests have passed
        print("All tests passed!")

# If this script is run as the main program (not imported as a module), run the tests
if __name__ == "__main__":
    test_case = MainViewsTestCase()
    test_case.run_all_tests()
