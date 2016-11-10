import doctest
import unittest
from plone.testing import layered
from collective.gtags.base import FUNCTIONAL_TESTING


def setUp(test):
    pass
        
def tearDown(test):
    setup.placefulTearDown()
    
def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            doctest.DocFileSuite(
                'tagging.txt',
                optionflags=doctest.ELLIPSIS
            ),
            layer=FUNCTIONAL_TESTING
        ),
        layered(
            doctest.DocFileSuite(
                'behaviors.txt',
                optionflags=doctest.ELLIPSIS
            ),
            layer=FUNCTIONAL_TESTING
        ),
    ])
    return suite
if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')