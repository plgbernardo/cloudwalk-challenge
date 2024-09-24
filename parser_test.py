import unittest
from unittest.mock import mock_open, patch
from parser import *

class TestParseLog(unittest.TestCase):
    
    # Simulate a short game log and set a desired output format.
    def setUp(self):
        self.sample_log_data = r"""
        InitGame: \sv_floodProtect\0\sv_maxPing\0\sv_minPing\0\sv_maxRate
        ClientUserinfoChanged: 2 n\Player1\t\0\model\uriel/zael\hmodel\uriel/zael
        ClientUserinfoChanged: 3 n\Player2\t\0\model\sarge\hmodel\sarge\g_redteam
        Kill: 1022 2 6: <world> killed Player1 by MOD_FALLING
        Kill: 3 2 7: Player2 killed Player1 by MOD_ROCKET
        ShutdownGame:
        """

        self.expected_result = {
            "game_1": {
                "total_kills": 2,
                "players": ["Player1", "Player2"],
                "kills": {
                    "Player1": 0,
                    "Player2": 1
                }
            }
        }

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_parse_log_basic(self, mock_file):
        # Test parse_log function with mock string data.
        mock_file.return_value.read.return_value = self.sample_log_data
        result = parse_log(self.sample_log_data)

        # Sort players list before comparison.
        result["game_1"]["players"].sort()
        self.expected_result["game_1"]["players"].sort()

        self.assertEqual(result, self.expected_result)

    def test_process_kill_event(self):
        # Create a mock game state and a kill event line.
        current_match = {"total_kills": 0, "players": set(), "kills_data": {}}
        line = "Kill: 3 2 7: Player2 killed Player1 by MOD_ROCKET"
        
        # Manually simulate process_kill_event on total_kills.
        current_match["total_kills"] += 1
        process_kill_event(current_match, line)
        
        # Check if the kill event was processed correctly.
        self.assertEqual(current_match["total_kills"], 1)
        self.assertIn("Player1", current_match["players"])
        self.assertIn("Player2", current_match["kills_data"])
        self.assertEqual(current_match["kills_data"]["Player2"], 1)

    def test_process_match(self):
        # Simulate a game state with a list of players.
        current_match = {
            "total_kills": 2,
            "players": ["Player1", "Player2"],
            "kills_data": {"Player1": 0, "Player2": 1}
        }
        matches_data = {}
        process_match(current_match, matches_data)
        
        # Sort players list in the match data before comparison
        matches_data["game_1"]["players"].sort()
        
        # Check if the match was processed correctly
        self.assertEqual(matches_data["game_1"]["total_kills"], 2)
        self.assertEqual(matches_data["game_1"]["players"], ["Player1", "Player2"])
        self.assertEqual(matches_data["game_1"]["kills"]["Player1"], 0)
        self.assertEqual(matches_data["game_1"]["kills"]["Player2"], 1)


    def test_add_player(self):
        # Create a mock game state and simulate a player joining the game.
        current_match = {"total_kills": 0, "players": set(), "kills_data": {}}
        line = r"ClientUserinfoChanged: 2 n\Player1\t\0\model\uriel/zael\hmodel\uriel/zael"
        add_player(current_match, line)
        
        # Check if the player was added correctly.
        self.assertIn("Player1", current_match["players"])
        self.assertIn("Player1", current_match["kills_data"])
        self.assertEqual(current_match["kills_data"]["Player1"], 0)

if __name__ == "__main__":
    unittest.main()
