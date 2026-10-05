import unittest
from scanner import parse_ports 
from scanner import resolve_target
from scanner import scan_port
class testing(unittest.TestCase):
    def test_specific_port(self):
        self.assertEqual(parse_ports("80"),[80])
    def test_range_ports(self):
        self.assertEqual(list(parse_ports("1-5")),[1,2,3,4,5])
    def test_chosen_ports(self):
        self.assertEqual(parse_ports("225,443,80"),[225,443,80])
    def test_invalid_ports(self):
        self.assertEqual(parse_ports("abc"),None)
    def test_zero_ports(self):
        self.assertEqual(parse_ports("0"),None)
    def test_ports_above_max(self):
        self.assertEqual(parse_ports("65700"),None)
    def test_resolving_target(self):
        self.assertIsNotNone(resolve_target("google.com"))
    def test_invalid_host_target(self):
        self.assertEqual(resolve_target("abcdeasdf.com"),None)
    def test_open_port(self):
        result = scan_port("127.0.0.1",2223)
        self.assertEqual(result['status'],"open")
    def test_close_port(self):
        result = scan_port("127.0.0.1",2227)
        self.assertEqual(result['status'],"closed")
if __name__ == "__main__":
    unittest.main()
