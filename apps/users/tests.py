from django.test import TestCase

# Create your tests here.
import uuid
random = str(uuid.uuid1())
code = random[0:16]
code=code.replace('-','')
print(random,code)
