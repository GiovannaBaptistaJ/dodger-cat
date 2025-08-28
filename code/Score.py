# IMPORTS
import os

class Score:
    FILE_PATH = "./scores.txt"
    TOP_N = 10  # maximum amount of scores

    def __init__(self):
        self.scores = self.load_scores()

    def load_scores(self):
        if not os.path.exists(self.FILE_PATH):
            return []
        with open(self.FILE_PATH, "r") as f:
            scores = [int(line.strip()) for line in f if line.strip().isdigit()]
        return sorted(scores, reverse=True)[:self.TOP_N]

    def add_score(self, score: int):
        self.scores.append(score)
        self.scores = sorted(self.scores, reverse=True)[:self.TOP_N]
        with open(self.FILE_PATH, "w") as f:
            for s in self.scores:
                f.write(f"{s}\n")

    def get_scores(self):
        return self.scores
