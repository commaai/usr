import unittest
from recordclass.memoryslots import memoryslots
try:
    from test import support, seq_tests
except:
    from test import test_support as support, seq_tests

import gc
import pickle

class MemorySlotsTest(unittest.TestCase):
    type2test = memoryslots

    def test_constructors(self):
        #super().test_constructors()
        # calling built-in types without argument must return empty
        self.assertEqual(memoryslots(), ())
        self.assertEqual(memoryslots([]), memoryslots([]))
        self.assertEqual(memoryslots(0, 1, 2, 3), memoryslots(0, 1, 2, 3))
        self.assertEqual(memoryslots(''), memoryslots(''))

    def test_truth(self):
        #super().test_truth()
        self.assertTrue(not memoryslots())
        self.assertTrue(memoryslots([42]))

    def test_len(self):
        #super().test_len()
        self.assertEqual(len(memoryslots()), 0)
        self.assertEqual(len(memoryslots(0)), 1)
        self.assertEqual(len(memoryslots(0, 1, 2)), 3)

    def test_memoryslotsresizebug(self):
        # Check that a specific bug in _PyTuple_Resize() is squashed.
        def f():
            for i in range(1000):
                yield i
        self.assertEqual(list(memoryslots(*f())), list(range(1000)))
 
    def test_repr(self):
        l0 = memoryslots()
        l2 = memoryslots(0, 1, 2)
        a0 = self.type2test(*l0)
        a2 = self.type2test(*l2)

        self.assertEqual(str(a0), repr(l0))
        self.assertEqual(str(a2), repr(l2))
        self.assertEqual(repr(a0), "memoryslots()")
        self.assertEqual(repr(a2), "memoryslots(0, 1, 2)")

    def _not_tracked(self, t):
        # Nested memoryslotss can take several collections to untrack
        gc.collect()
        gc.collect()
        self.assertFalse(gc.is_tracked(t), t)

    def _tracked(self, t):
        self.assertTrue(gc.is_tracked(t), t)
        gc.collect()
        gc.collect()
        self.assertTrue(gc.is_tracked(t), t)

    def test_repr_large(self):
        # Check the repr of large list objects
        def check(n):
            l = (0,) * n
            s = repr(l)
            self.assertEqual(s,
                '(' + ', '.join(['0'] * n) + ')')
        check(10)       # check our checking code
        check(1000000)
    
    def test_iterator_pickle(self):
        # Userlist iterators don't support pickling yet since
        # they are based on generators.
        data = self.type2test([4, 5, 6, 7])
        for proto in range(pickle.HIGHEST_PROTOCOL + 1):
            itorg = iter(data)
            d = pickle.dumps(itorg, proto)
            it = pickle.loads(d)
            self.assertEqual(type(itorg), type(it))
            self.assertEqual(self.type2test(*it), self.type2test(data))

        it = pickle.loads(d)
        next(it)
        d = pickle.dumps(it)
        self.assertEqual(self.type2test(*it), self.type2test(data)[1:])

    # def test_reversed_pickle(self):
    #     data = self.type2test([4, 5, 6, 7])
    #     for proto in range(pickle.HIGHEST_PROTOCOL + 1):
    #         itorg = reversed(data)
    #         d = pickle.dumps(itorg, proto)
    #         it = pickle.loads(d)
    #         self.assertEqual(type(itorg), type(it))
    #         self.assertEqual(self.type2test(*it), self.type2test(reversed(data)))
    #
    #         it = pickle.loads(d)
    #         next(it)
    #         d = pickle.dumps(it, proto)
    #         self.assertEqual(self.type2test(*it), self.type2test(reversed(data))[1:])

    def test_no_comdat_folding(self):
        # Issue 8847: In the PGO build, the MSVC linker's COMDAT folding
        # optimization causes failures in code that relies on distinct
        # function addresses.
        class T(memoryslots): pass
        with self.assertRaises(TypeError):
            [3,] + T((1,2))

def main():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MemorySlotsTest))
    return suite

