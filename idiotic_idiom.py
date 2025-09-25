import random
import streamlit as st

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
        "while humming loudly", "before lunch", "after midnight", "on roller skates", "inside a dream",
        "is a game well played"
    ]

    return f"{random.choice(subjects)} {random.choice(verbs)} {random.choice(adjectives)} {random.choice(objects)} {random.choice(endings)}."

def render_idiom_badge(st):
    if "last_idiom" not in st.session_state:
        st.session_state.last_idiom = ""

    if st.button("🎲 Generate Idiotic Idiom"):
        new_idiom = generate_idiom()

        # Ensure no immediate repetition
        while new_idiom == st.session_state.last_idiom:
            new_idiom = generate_idiom()

        st.session_state.last_idiom = new_idiom
        st.success(f"💡 Idiotic Idiom: {new_idiom}")

# Quick standalone test
if __name__ == "__main__":
    last = ""
    for _ in range(5):
        idiom = generate_idiom()
        while idiom == last:
            idiom = generate_idiom()
        last = idiom
        print("💡 Idiotic Idiom:", idiom)
