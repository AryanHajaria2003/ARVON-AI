import streamlit as st

from Rag_pipeline import generate_answer


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ARVON AI | Freshwork RAG Assistant",
    page_icon="🔥",
    layout="wide"
)


# ============================================================
# APP DETAILS + LINKS
# ============================================================

APP_NAME = "ARVON AI"
APP_SUBTITLE = "XYZ Company RAG Assistant"
AUTHOR = "Aryan Hajaria"

GITHUB = "https://github.com/AryanHajaria2003"
LINKEDIN = "https://www.linkedin.com/in/aryan-hajaria-466a54318/"

GITHUB_SVG = (
    '<svg viewBox="0 0 24 24" aria-hidden="true">'
    '<path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/>'
    '</svg>'
)

LINKEDIN_SVG = (
    '<svg viewBox="0 0 24 24" aria-hidden="true">'
    '<path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>'
    '</svg>'
)


# ============================================================
# RAG FUNCTION
# ============================================================

def rag_answer(query):

    answer, sources = generate_answer(query)

    return answer, sources


# ============================================================
# HTML HELPER
# ============================================================

def flat(html):
    """Strip indentation and blank lines so Markdown never
    turns the HTML into a code block."""

    return " ".join(
        line.strip() for line in html.splitlines() if line.strip()
    )


# ============================================================
# CUSTOM CSS
# ============================================================

STYLE = """
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Syne:wght@600;700;800&display=swap');

:root {
    --bg: #070404;
    --box: #0d0706;
    --panel: #150b09;
    --edge: #3a1c14;
    --accent: #ff5a2c;
    --accent-hot: #ff7a3d;
    --accent-deep: #b8310f;
    --text: #f4ebe6;
    --muted: #a8938a;
}

/* ---------- Page ---------- */

html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}

.stApp {
    background:
        radial-gradient(900px 420px at 50% -120px, rgba(255, 90, 44, .16), transparent 70%),
        var(--bg);
}

#MainMenu,
footer,
header[data-testid="stHeader"] {
    visibility: hidden;
    height: 0;
}

/* ---------- The main box ---------- */

.block-container,
[data-testid="stMainBlockContainer"] {
    max-width: 960px;
    margin: 1.6rem auto 4.5rem;
    padding: 2rem 2rem 2rem;
    background: var(--box);
    border: 1px solid var(--edge);
    border-top: 2px solid var(--accent);
    border-radius: 22px;
    box-shadow:
        0 0 0 6px rgba(255, 90, 44, .04),
        0 30px 80px rgba(0, 0, 0, .65),
        0 0 70px rgba(255, 90, 44, .08);
}

/* ---------- Header ---------- */

.topbar {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: start;
    margin-bottom: 1.8rem;
}

.brand {
    grid-column: 2;
    text-align: center;
}

.brand h1 {
    margin: 0;
    padding: 0 0 0 .2em;           /* balances trailing letter-spacing */
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 3.1rem;
    letter-spacing: .2em;
    line-height: 1.05;
    color: var(--text);
}

.brand p {
    margin: .65rem 0 0;
    font-size: .95rem;
    font-weight: 500;
    letter-spacing: .08em;
    color: var(--accent);
}

.socials {
    grid-column: 3;
    justify-self: end;
    display: flex;
    gap: .5rem;
    padding: .4rem;
    border: 1px solid var(--edge);
    border-radius: 999px;
    background: var(--panel);
}

.socials a {
    display: grid;
    place-items: center;
    width: 42px;
    height: 42px;
    border-radius: 50%;
    background: #231210;
    color: var(--text) !important;
    text-decoration: none !important;
    transition: background .18s, color .18s, transform .18s;
}

.socials a:hover {
    background: var(--accent);
    color: #1a0805 !important;
    transform: translateY(-2px);
}

.socials a:focus-visible {
    outline: 2px solid var(--accent-hot);
    outline-offset: 2px;
}

.socials svg {
    width: 20px;
    height: 20px;
    fill: currentColor;
}

@media (max-width: 700px) {
    .block-container,
    [data-testid="stMainBlockContainer"] {
        margin: .8rem .6rem 4.5rem;
        padding: 1.2rem 1rem;
    }
    .topbar { grid-template-columns: 1fr; gap: 1rem; }
    .brand, .socials { grid-column: 1; }
    .socials { justify-self: center; }
    .brand h1 { font-size: 2.1rem; }
}

/* ---------- Question bar ---------- */

[data-testid="stChatInput"] {
    background: var(--panel);
    border: 1px solid var(--accent-deep);
    border-radius: 14px;
    transition: border-color .15s, box-shadow .15s;
}

[data-testid="stChatInput"]:focus-within {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(255, 90, 44, .18);
}

[data-testid="stChatInput"] textarea {
    background: transparent;
    color: var(--text);
}

[data-testid="stChatInput"] button {
    background: var(--accent);
    color: #1a0805;
}

/* ---------- Conversation box ---------- */

[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--panel);
    border: 1px solid var(--edge);
    border-radius: 16px;
}

[data-testid="stChatMessage"] {
    background: #1c0f0c;
    border: 1px solid var(--edge);
    border-radius: 12px;
}

[data-testid="stChatMessageAvatarUser"] {
    background: var(--accent);
}

[data-testid="stChatMessageAvatarAssistant"] {
    background: var(--accent-deep);
}

[data-testid="stExpander"] {
    background: var(--panel);
    border: 1px solid var(--edge);
    border-radius: 10px;
}

[data-testid="stCaptionContainer"] {
    color: var(--muted);
}

code {
    color: var(--accent-hot);
    background: #26120d;
}

/* ---------- Footer ---------- */

.byline {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    text-align: center;
    padding: .55rem 0 .8rem;
    font-size: .85rem;
    color: var(--muted);
    background: linear-gradient(to top, var(--bg) 70%, transparent);
    pointer-events: none;
    z-index: 5;
}

.byline b {
    color: var(--accent);
    font-weight: 600;
    letter-spacing: .08em;
}

</style>
"""

HEADER = f"""
<div class="topbar">

    <div class="brand">
        <h1>{APP_NAME}</h1>
        <p>{APP_SUBTITLE}</p>
    </div>

    <div class="socials">
        <a href="{GITHUB}" target="_blank" rel="noopener"
           aria-label="GitHub" title="GitHub">{GITHUB_SVG}</a>
        <a href="{LINKEDIN}" target="_blank" rel="noopener"
           aria-label="LinkedIn" title="LinkedIn">{LINKEDIN_SVG}</a>
    </div>

</div>
"""

st.markdown(
    flat(STYLE + HEADER),
    unsafe_allow_html=True
)


# ============================================================
# LAYOUT: input bar on top, conversation box underneath
# ============================================================

# st.chat_input is pinned to the bottom of the page by default.
# Placing it inside a container keeps it inline, right under the header.

input_area = st.container()

# Bordered, fixed-height box that scrolls when the chat gets long.
chat_area = st.container(height=440, border=True)

with input_area:

    prompt = st.chat_input("Ask a Question")


# ============================================================
# CHAT MEMORY
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


with chat_area:

    # --------------------------------------------------------
    # INITIAL MESSAGE
    # --------------------------------------------------------

    if not st.session_state.messages and not prompt:

        st.caption(
            "Ask a question about the Freshworks document collection."
        )


    # --------------------------------------------------------
    # DISPLAY PREVIOUS MESSAGES
    # --------------------------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(
                message["content"]
            )

            # Display sources if available
            if message.get("sources"):

                with st.expander("Sources"):

                    for i, doc in enumerate(
                        message["sources"],
                        1
                    ):

                        source = doc.metadata.get(
                            "source",
                            "Unknown"
                        )

                        page = doc.metadata.get(
                            "page",
                            "N/A"
                        )

                        st.markdown(
                            f"**{i}.** `{source}` — Page `{page}`"
                        )


    # --------------------------------------------------------
    # NEW QUESTION
    # --------------------------------------------------------

    if prompt:

        # User message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):

            st.markdown(prompt)


        # Assistant response
        with st.chat_message("assistant"):

            with st.spinner(
                "Searching Freshworks documents..."
            ):

                try:

                    answer, sources = rag_answer(
                        prompt
                    )

                    st.markdown(answer)

                    # Sources
                    with st.expander("Sources"):

                        for i, doc in enumerate(
                            sources,
                            1
                        ):

                            source = doc.metadata.get(
                                "source",
                                "Unknown"
                            )

                            page = doc.metadata.get(
                                "page",
                                "N/A"
                            )

                            st.markdown(
                                f"**{i}.** `{source}` — Page `{page}`"
                            )

                    # Save assistant response
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "sources": sources
                        }
                    )

                except Exception as e:

                    error_message = (
                        f"Something went wrong: `{e}`"
                    )

                    st.error(error_message)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": error_message
                        }
                    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    f'<div class="byline">by <b>{AUTHOR.upper()}</b></div>',
    unsafe_allow_html=True
)
