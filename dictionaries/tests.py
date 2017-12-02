from django.test import TestCase

from . import models


class ModelTestCase(TestCase):
    """This class defines the test suite for the dictionary model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.dictionary_name = "Write world class code"
        self.dictionary = models.Dictionary(name=self.dictionary_name)

    def test_model_can_create_a_dictionary(self):
        """Test the dictionary model can create a dictionary."""
        old_count = models.Dictionary.objects.count()
        self.dictionary.save()
        new_count = models.Dictionary.objects.count()
        self.assertNotEqual(old_count, new_count)
