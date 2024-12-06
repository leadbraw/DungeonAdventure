import pickle


class GameStateManager:

    @staticmethod
    def get_instance():
        """Static method to fetch the singleton instance."""
        if GameStateManager._instance is None:
            GameStateManager._instance = GameStateManager()
        return GameStateManager._instance

    @staticmethod
    def load_game_state():
        """
        Loads the saved game state from save.pkl file.
        :return: a saved instance of game_controller.
        """
        with open('save.pkl', 'rb') as f:
            state = pickle.load(f)
        return state

    @staticmethod
    def save_game_state(game_controller_instance):
        """
        Saves the current game state to save.pkl file.
        :param game_controller_instance: a game_controller instance.
        """
        # TODO change location of save file
        with open('save.pkl', 'wb') as f:
            pickle.dump(game_controller_instance, f)