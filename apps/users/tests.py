from django.test import TestCase

# Create your tests here.
import uuid
random = str(uuid.uuid1())
code = random[0:8]
print(random,code)
