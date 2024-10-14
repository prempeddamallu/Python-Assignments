
from abc import ABC, abstractmethod

class Person(ABC):
    """Abstract base class representing a person."""
    
    @abstractmethod
    def get_gender(self):
        """Abstract method that should return the gender."""
        pass

class Male(Person):
    
    def get_gender(self):
        return "Male"

class Female(Person):
    
    def get_gender(self):
        return "Female"
    
try:
    # Attempting to create an instance of Person should raise an error
    p = Person()  # This will raise an error
except TypeError as e:
    print(f"Error: {e}")

# Create instances of Male and Female
male = Male()
female = Female()

print(male.get_gender())  # Output: Male
print(female.get_gender())  # Output: Female


