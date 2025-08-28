from abc import ABC, abstractmethod

class AbstractLabTestDAO(ABC):
    """
    Abstract DAO for Lab Tests
    """

    # counter for auto-increment
    _counter = 0
    _prefix = "TEST"

    @classmethod
    def generate_test_id(cls):
        """
        Auto-generate lab test IDs like TEST0001, TEST0002...
        """
        cls._counter += 1
        return f"{cls._prefix}{cls._counter:04d}"

    @abstractmethod
    def create_labtest(self, labtest):
        pass

    @abstractmethod
    def update_labtest(self, test_id, labtest):
        pass

    @abstractmethod
    def deactivate_labtest(self, test_id):
        pass

    @abstractmethod
    def get_labtest_by_id(self, test_id):
        pass

    @abstractmethod
    def list_labtests(self):
        pass
