import random

def render_idiom_badge(st):
    # Keep idiom result in session state so it doesn't vanish on rerun
    if "idiom" not in st.session_state:
        st.session_state.idiom = None

    # Button generates a new idiom
    if st.button("🎲 Generate Idiotic Idiom"):
        subjects = [
            "a frog", "teacher", "no sandwich", "a cloud", "my toothbrush",
            "a penguin", "this laptop", "my neighbor’s cat", "an elevator", "a cactus"
        ]
        verbs = [
            "jumps over", "complains about", "tickles", "dances with", "argues with",
            "confuses", "balances on", "runs away from", "interviews", "ignores"
        ]
        objects = [
            "the moon", "a spatula", "quantum foam", "regret", "a lazy river",
            "traffic cones", "a potato chip", "the stock market", "a shoelace", "jellybeans"
        ]
        endings = [
            "on Thursdays", "without warning", "if nobody watches", "in traffic", "during tax season",
            "while humming loudly", "before lunch", "after midnight", "on roller skates", "inside a dream"
        ]

        st.session_state.idiom = (
            f"{random.choice(subjects)} {random.choice(verbs)} "
            f"{random.choice(objects)} {random.choice(endings)}."
        )

    # Show idiom if it exists
    if st.session_state.idiom:
        st.success(f"💡 Idiotic Idiom: {st.session_state.idiom}")