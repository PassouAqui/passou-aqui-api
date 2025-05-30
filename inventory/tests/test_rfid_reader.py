from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from inventory.models import RFIDReader, Location # Assuming Location might be needed for ForeignKey
from inventory.serializers import RFIDReaderSerializer # For potential direct serializer tests or reference

class RFIDReaderViewSetTests(APITestCase):
    def setUp(self):
        # It's good practice to create any dependent objects here if needed
        # For example, if RFIDReader had a required ForeignKey to Location:
        self.location = Location.objects.create(name="Test Location Central")
        self.rfid_reader_data = {
            'name': 'Reader 1',
            'description': 'Main entrance reader',
            'ip_address': '192.168.1.100',
            'mac_address': '00:1A:2B:3C:4D:5E',
            'serial_number': 'SN123456789',
            'location': self.location.id 
        }
        self.rfid_reader_list_url = reverse('rfidreader-list') # Assuming basename 'rfidreader'

    def test_create_rfid_reader(self):
        """
        Ensure we can create a new RFIDReader object.
        """
        response = self.client.post(self.rfid_reader_list_url, self.rfid_reader_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RFIDReader.objects.count(), 1)
        reader = RFIDReader.objects.get()
        self.assertEqual(reader.name, 'Reader 1')
        self.assertEqual(str(reader.location), self.location.name)

    def test_retrieve_rfid_reader(self):
        """
        Ensure we can retrieve an RFIDReader object.
        """
        # First, create a reader
        response_create = self.client.post(self.rfid_reader_list_url, self.rfid_reader_data, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        reader_id = response_create.data['id']
        
        detail_url = reverse('rfidreader-detail', kwargs={'pk': reader_id})
        response_retrieve = self.client.get(detail_url, format='json')
        self.assertEqual(response_retrieve.status_code, status.HTTP_200_OK)
        self.assertEqual(response_retrieve.data['name'], self.rfid_reader_data['name'])

    def test_update_rfid_reader(self):
        """
        Ensure we can update an RFIDReader object.
        """
        # Create a reader
        response_create = self.client.post(self.rfid_reader_list_url, self.rfid_reader_data, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        reader_id = response_create.data['id']
        
        updated_data = self.rfid_reader_data.copy()
        updated_data['name'] = 'Reader 1 Updated'
        updated_data['ip_address'] = '192.168.1.101'
        
        detail_url = reverse('rfidreader-detail', kwargs={'pk': reader_id})
        response_update = self.client.put(detail_url, updated_data, format='json')
        
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(response_update.data['name'], 'Reader 1 Updated')
        self.assertEqual(response_update.data['ip_address'], '192.168.1.101')
        
        # Verify in DB
        updated_reader = RFIDReader.objects.get(id=reader_id)
        self.assertEqual(updated_reader.name, 'Reader 1 Updated')

    def test_delete_rfid_reader(self):
        """
        Ensure we can delete an RFIDReader object.
        """
        # Create a reader
        response_create = self.client.post(self.rfid_reader_list_url, self.rfid_reader_data, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        reader_id = response_create.data['id']
        
        detail_url = reverse('rfidreader-detail', kwargs={'pk': reader_id})
        response_delete = self.client.delete(detail_url)
        
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(RFIDReader.objects.count(), 0) # Assumes hard delete for this test for simplicity
                                                        # If using soft delete, check for is_deleted or similar
                                                        # For SoftDeleteObject, it means objects.count() should be 0.
                                                        # To check soft-deleted items: RFIDReader.all_objects.count()

    def test_list_rfid_readers(self):
        """
        Ensure we can list RFIDReader objects.
        """
        # Create a couple of readers
        self.client.post(self.rfid_reader_list_url, self.rfid_reader_data, format='json')
        data2 = self.rfid_reader_data.copy()
        data2['name'] = 'Reader 2'
        data2['serial_number'] = 'SN987654321'
        self.client.post(self.rfid_reader_list_url, data2, format='json')
        
        response_list = self.client.get(self.rfid_reader_list_url, format='json')
        self.assertEqual(response_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_list.data), 2) # Or response_list.data['count'] if paginated

    # TODO: Add tests for field validations if time permits
    # e.g., required fields, unique serial number, valid IP/MAC formats.
    # Example for serial number uniqueness:
    # def test_create_rfid_reader_duplicate_serial(self):
    #     self.client.post(self.rfid_reader_list_url, self.rfid_reader_data, format='json') # First reader
    #     response = self.client.post(self.rfid_reader_list_url, self.rfid_reader_data, format='json') # Second with same SN
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn('serial_number', response.data) # Check if 'serial_number' field has an error
    #     self.assertEqual(RFIDReader.objects.count(), 1)

# It's also good to have a separate test class for Serializer logic if it's complex,
# but for basic ModelSerializer, ViewSet tests often cover serializer validation indirectly.

# class RFIDReaderSerializerTests(APITestCase): # Or Django's TestCase if not hitting DB much
#     def test_serializer_with_valid_data(self):
#         location = Location.objects.create(name="Test Location for Serializer")
#         valid_data = {
#             'name': 'Reader S1', 'serial_number': 'SNSERIAL1', 'location': location.id
#         }
#         serializer = RFIDReaderSerializer(data=valid_data)
#         self.assertTrue(serializer.is_valid())
#         reader = serializer.save()
#         self.assertEqual(reader.name, 'Reader S1')

#     def test_serializer_missing_required_field(self):
#         invalid_data = {'serial_number': 'SNSERIAL2'} # Missing name
#         serializer = RFIDReaderSerializer(data=invalid_data)
#         self.assertFalse(serializer.is_valid())
#         self.assertIn('name', serializer.errors)

# Note: The basename for reverse URL generation needs to match what's in urls.py
# For `router.register(r'rfid-readers', RFIDReaderViewSet)`, the basename is 'rfidreader'
# if not explicitly set with `basename='...'`. Django REST Framework usually infers it.
# If `RFIDReaderViewSet` has `queryset = RFIDReader.objects.all()`, then DRF can infer basename.
# The `rfid-readers` path was added as `router.register(r'rfid-readers', RFIDReaderViewSet)`
# This means the basename should be 'rfidreader'. So, 'rfidreader-list' and 'rfidreader-detail'.
# I used this in `setUp`.
# For this to run, an __init__.py file might be needed in inventory/tests/
# Also, the test runner needs to find this app and its tests.
# This typically involves ensuring 'inventory' is in INSTALLED_APPS.
# The database connection issue from previous steps might affect test runs.
# Django's test runner usually creates a test database.
# If it tries to use the main 'rfid' PostgrSQL DB and it's down, tests will fail at setup.
# If it uses an in-memory SQLite for tests (common default if no specific test DB config),
# these tests might pass even if the main PostgreSQL DB is down.
# The `SoftDeleteObject` logic means that after a delete, `RFIDReader.objects.count()` will be 0.
# `RFIDReader.all_objects.count()` would be 1 if it were soft-deleted and not hard-deleted.
# Standard ModelViewSet delete performs a hard delete unless the model's delete() is overridden
# by SoftDeleteObject to perform a soft delete, which it does.
# So, `RFIDReader.objects.count()` (which uses the default manager filtering non-deleted) should be 0.
# `RFIDReader.all_objects.count()` (which uses the manager that sees all objects) would be 1.
# The test `test_delete_rfid_reader` currently asserts `RFIDReader.objects.count() == 0`. This is correct.
