# score.py

class Score:
    def __init__(self):
        self.score = 0
    
    def increase(self):
        """Increase the score by 1."""
        self.score += 10
    
    def get_score(self):
        """Return the current score."""
        return self.score
