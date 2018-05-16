# {{LICENCE}}

from recordclass.test.test_record import *
from recordclass.test.test_memoryslots import *

def test_all():
    import unittest
    unittest.main(verbosity=2)
