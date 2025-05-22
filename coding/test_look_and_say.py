import unittest
from look_and_say import center_two_digits, nth_term

class TestLookAndSay(unittest.TestCase):
    
    def test_get_nth_term(self):
        """get_nth_term 함수의 정확성을 테스트합니다."""
        self.assertEqual(nth_term(1), "1")
        self.assertEqual(nth_term(2), "11")
        self.assertEqual(nth_term(3), "21")
        self.assertEqual(nth_term(4), "1211")
        self.assertEqual(nth_term(5), "111221")
        self.assertEqual(nth_term(6), "312211")
        self.assertEqual(nth_term(7), "13112221")
        self.assertEqual(nth_term(8), "1113213211")
    

    def test_solution(self):
        """solution 함수의 정확성을 테스트합니다."""
        self.assertEqual(center_two_digits(5), "12")
        self.assertEqual(center_two_digits(8), "21")
    

if __name__ == "__main__":
    unittest.main()