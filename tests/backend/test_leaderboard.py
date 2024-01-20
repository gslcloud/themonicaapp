import unittest
from my_app import make_donation, get_leaderboard, clear_donations, clear_leaderboard

class TestLeaderboard(unittest.TestCase):
    def setUp(self):
        # Clear any existing donations and leaderboard data before each test
        clear_donations()
        clear_leaderboard()

    def test_leaderboard_order(self):
        """
        Test that the leaderboard orders the donors correctly based on total donation amount.
        """
        # Simulate donations made by the donors with different amounts
        make_donation('Donor1', amount=100)
        make_donation('Donor2', amount=200)
        make_donation('Donor3', amount=150)
        make_donation('Donor4', amount=50)
        make_donation('Donor5', amount=300)

        # Get the leaderboard
        leaderboard = get_leaderboard()

        # Verify that the leaderboard orders the donors correctly
        expected_leaderboard = ['Donor5', 'Donor2', 'Donor3', 'Donor1', 'Donor4']
        self.assertEqual(leaderboard, expected_leaderboard)

    def test_leaderboard_limit(self):
        """
        Test that the leaderboard only includes the top N donors.
        """
        # Set the leaderboard limit to 3
        leaderboard_limit = 3

        # Simulate donations made by the donors
        make_donation('Donor1', amount=100)
        make_donation('Donor2', amount=200)
        make_donation('Donor3', amount=150)
        make_donation('Donor4', amount=50)

        # Get the leaderboard with the limit
        leaderboard = get_leaderboard(limit=leaderboard_limit)

        # Verify that the leaderboard includes the top N donors only
        expected_leaderboard = ['Donor2', 'Donor3', 'Donor1']
        self.assertEqual(leaderboard, expected_leaderboard)

    def test_clear_donations(self):
        """
        Test that the donations are cleared correctly.
        """
        # Simulate donations made by the donors
        make_donation('Donor1', amount=100)
        make_donation('Donor2', amount=200)

        # Clear the donations
        clear_donations()

        # Verify that the donations are cleared
        leaderboard = get_leaderboard()
        self.assertEqual(len(leaderboard), 0)

    def test_clear_leaderboard(self):
        """
        Test that the leaderboard is cleared correctly.
        """
        # Simulate donations made by the donors
        make_donation('Donor1', amount=100)
        make_donation('Donor2', amount=200)

        # Clear the leaderboard
        clear_leaderboard()

        # Verify that the leaderboard is cleared
        leaderboard = get_leaderboard()
        self.assertEqual(len(leaderboard), 0)

    def test_leaderboard_empty(self):
        """
        Test that the leaderboard is empty when there are no donations.
        """
        # Get the leaderboard without making any donations
        leaderboard = get_leaderboard()

        # Verify that the leaderboard is empty
        self.assertEqual(len(leaderboard), 0)

    def test_leaderboard_limit_greater_than_donors(self):
        """
        Test that the leaderboard includes all donors when the limit is greater than the number of donors.
        """
        # Set the leaderboard limit to a value greater than the number of donors
        leaderboard_limit = 10

        # Simulate donations made by the donors
        make_donation('Donor1', amount=100)
        make_donation('Donor2', amount=200)
        make_donation('Donor3', amount=150)

        # Get the leaderboard with the limit
        leaderboard = get_leaderboard(limit=leaderboard_limit)

        # Verify that the leaderboard includes all donors
        expected_leaderboard = ['Donor2', 'Donor3', 'Donor1']
        self.assertEqual(leaderboard, expected_leaderboard)

if __name__ == '__main__':
    unittest.main()