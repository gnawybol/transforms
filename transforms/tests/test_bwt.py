import unittest

from transforms.reordering import BWT


class BwtTests(unittest.TestCase):

    def test_forward_of_banana(self):
        expected_bytes = b'banana'
        forward = BWT.forward(expected_bytes)
        # According to http://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform
        assert forward.startswith(b'bnnaaa')
        # Final byte is start byte
        assert len(forward) == len(expected_bytes) + 1

    def test_forward_and_inverse_of_banana(self):
        expected_bytes = b'banana'
        forward = BWT.forward(expected_bytes)
        inverse = BWT.inverse(forward)
        assert inverse == expected_bytes

    def test_forward_and_inverse_lorem_ipsum(self):
        # region expected bytes (lorem ipsum)
        expected_bytes = \
b'''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eget elementum ligula. Aliquam erat volutpat.
Donec interdum vulputate elit, id condimentum leo maximus sit amet. Suspendisse ligula massa, sollicitudin a
faucibus sit amet, vulputate at arcu. Praesent eget purus id leo laoreet vulputate. Lorem ipsum dolor sit amet,
consectetur adipiscing elit. Duis nec turpis faucibus, fringilla eros at, auctor nisi. Fusce quis elementum felis.
Vestibulum blandit augue sed laoreet ultricies. Nam porttitor cursus quam sed laoreet. Nunc est elit, sagittis a
nisl sed, convallis luctus tortor. Etiam vel lorem a ligula gravida vehicula. Integer in pellentesque mauris.
Donec semper lectus ante, ut sollicitudin mi interdum vitae.'''
        # endregion
        forward = BWT.forward(expected_bytes)
        inverse = BWT.inverse(forward)
        assert inverse == expected_bytes
