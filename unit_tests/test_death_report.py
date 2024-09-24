import unittest
from unittest.mock import mock_open, patch
from death_report import *

class TestParseLogWithMOD(unittest.TestCase):

    # Simulate a short game log and set a desired output format.
    def setUp(self):
        self.sample_log_data = r"""
        InitGame: \sv_floodProtect\0\sv_maxPing\0\sv_minPing\0\sv_maxRate
        Kill: 1022 2 6: <world> killed Player1 by MOD_FALLING
        Kill: 3 2 7: Player2 killed Player1 by MOD_ROCKET
        ShutdownGame:
        InitGame: \sv_floodProtect\0\sv_maxPing\0\sv_minPing\0\sv_maxRate
        Kill: 4 3 7: Player3 killed Player2 by MOD_RAILGUN
        Kill: 2 4 6: Player1 killed Player3 by MOD_ROCKET
        ShutdownGame:
        """

        self.expected_result = {
            "game_1": {
                "kills_by_means": {
                    "MOD_FALLING": 1,
                    "MOD_ROCKET": 1
                }
            },
            "game_2": {
                "kills_by_means": {
                    "MOD_RAILGUN": 1,
                    "MOD_ROCKET": 1
                }
            }
        }

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_parse_log_with_mod(self, mock_file):
        # Mock the file reading operation with sample log data.
        mock_file.return_value.read.return_value = self.sample_log_data
        
        # Call the parse_log function and verify the result matches the expected output.
        result = parse_log(self.sample_log_data)
        self.assertEqual(result, self.expected_result)

    def test_process_kill_event(self):
        # Simulate a game in progress with empty means of death.
        current_match = {"kills_by_means": {}}
        line = "Kill: 3 2 7: Player2 killed Player1 by MOD_ROCKET"
        
        # Process the kill event and verify that MOD_ROCKET is counted correctly.
        process_kill_event(current_match, line)
        self.assertIn("MOD_ROCKET", current_match["kills_by_means"])
        self.assertEqual(current_match["kills_by_means"]["MOD_ROCKET"], 1)

    def test_process_match(self):
        # Simulate a match and ensure that it's processed into the match data structure.
        current_match = {
            "kills_by_means": {
                "MOD_FALLING": 1,
                "MOD_ROCKET": 2
            }
        }
        matches_data = {}
        
        # Process the match and verify that the match data is correctly stored.
        process_match(current_match, matches_data)
        self.assertIn("game_1", matches_data)
        self.assertEqual(matches_data["game_1"]["kills_by_means"]["MOD_FALLING"], 1)
        self.assertEqual(matches_data["game_1"]["kills_by_means"]["MOD_ROCKET"], 2)

if __name__ == "__main__":
    unittest.main()
