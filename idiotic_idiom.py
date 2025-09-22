import random

def generate_idiom():
    subjects = [
        "a frog", "teacher", "no sandwich", "a cloud", "my toothbrush",
        "a penguin", "this laptop", "my neighbor’s cat", "an elevator", "a cactus"
    ]
    verbs = [
        "jumps over", "complains about", "tickles", "dances with", "argues with",
        "confuses", "balances on", "runs away from", "interviews", "ignores"
    ]
    adjectives = [
        "soggy", "mysterious", "hyperactive", "glittery", "upside-down",
        "melancholy", "sticky", "ferocious", "dizzy", "lonely"
    ]
    objects = [
        "the moon", "a spatula", "quantum foam", "regret", "a lazy river",
        "traffic cones", "a potato chip", "the stock market", "a shoelace", "jellybeans"
    ]
    endings = [
        "on Thursdays", "without warning", "if nobody watches", "in traffic", "during tax season",
        "while humming loudly", "before lunch", "after midnight", "on roller skates", "inside a dream", "is a game well played"
    ]

    return f"A {random.choice(adjectives)} {random.choice(subjects)} {random.choice(verbs)} {random.choice(objects)} {random.choice(endings)}."

# Allow quick testing standalone
if __name__ == "__main__":
    for _ in range(5):
        print("💡 Idiotic Idiom:", generate_idiom())

