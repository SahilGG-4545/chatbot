import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage, AIMessage
import uuid

# ---- Page config (must be the very first Streamlit call) ----
st.set_page_config(
    page_title="LangGraph Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---- Global CSS + Animations ----
st.markdown("""
<style>
/* ═══════════════════════════════════════════════════
   KEYFRAME ANIMATIONS
═══════════════════════════════════════════════════ */

/* Gradient title hue shift */
@keyframes gradientShift {
    0%   { background-position: 0% 50%;   }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%;   }
}

/* Message bubble fade + slide up */
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0);    }
}

/* Floating bob for empty-state icon */
@keyframes floatBob {
    0%, 100% { transform: translateY(0px);   }
    50%       { transform: translateY(-12px); }
}

/* Shimmer sweep for New Chat button */
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position:  200% center; }
}

/* Sidebar active-thread glow pulse */
@keyframes glowPulse {
    0%, 100% { box-shadow: 0 0 0px rgba(130,100,255,0.0); }
    50%       { box-shadow: 0 0 8px rgba(130,100,255,0.7); }
}

/* Typing dots bounce */
@keyframes bounce {
    0%, 80%, 100% { transform: translateY(0);    opacity: 0.4; }
    40%           { transform: translateY(-6px); opacity: 1;   }
}

/* Radial background pulse on main canvas */
@keyframes bgPulse {
    0%, 100% { opacity: 0.03; }
    50%       { opacity: 0.07; }
}

/* ═══════════════════════════════════════════════════
   GLOBAL / MAIN AREA
═══════════════════════════════════════════════════ */

/* Subtle animated radial orb behind chat area */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    top: -30%;
    right: -20%;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(130,100,255,1) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
    animation: bgPulse 6s ease-in-out infinite;
    z-index: 0;
}

/* ═══════════════════════════════════════════════════
   ANIMATED GRADIENT TITLE
═══════════════════════════════════════════════════ */
.gradient-title {
    font-size: 1.9rem;
    font-weight: 800;
    background: linear-gradient(270deg, #a78bfa, #60a5fa, #34d399, #f472b6, #a78bfa);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientShift 5s ease infinite;
    margin-bottom: 0.1rem;
}

/* ═══════════════════════════════════════════════════
   CHAT MESSAGES — fade + slide in
═══════════════════════════════════════════════════ */
[data-testid="stChatMessage"] {
    animation: fadeSlideUp 0.35s ease both;
    border-radius: 12px;
    padding: 0.25rem 0.5rem;
    margin-bottom: 0.35rem;
}

/* ═══════════════════════════════════════════════════
   SIDEBAR
═══════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    padding-top: 1.5rem;
    border-right: 1px solid rgba(130,100,255,0.15);
}

/* All sidebar conversation buttons */
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    text-align: left;
    border-radius: 8px;
    padding: 0.45rem 0.75rem;
    font-size: 0.85rem;
    margin-bottom: 4px;
    border: 1px solid rgba(120,120,180,0.25);
    background: rgba(120,120,180,0.08);
    transition: background 0.2s, border-color 0.2s, transform 0.15s;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(120,120,180,0.22);
    border-color: rgba(130,100,255,0.6);
    transform: translateX(3px);
}

/* New Chat button — shimmer sweep on hover */
[data-testid="stSidebar"] .stButton:first-of-type > button {
    background: linear-gradient(
        90deg,
        rgba(130,100,255,0.15) 0%,
        rgba(255,255,255,0.25) 50%,
        rgba(130,100,255,0.15) 100%
    );
    background-size: 200% auto;
    border: 1px solid rgba(130,100,255,0.45);
    font-weight: 600;
    color: inherit;
}
[data-testid="stSidebar"] .stButton:first-of-type > button:hover {
    animation: shimmer 1.2s linear infinite;
    transform: none;
}

/* Active-thread button glow pulse */
[data-testid="stSidebar"] .stButton > button[kind="secondary"]:focus,
[data-testid="stSidebar"] .stButton > button:active {
    animation: glowPulse 1.8s ease-in-out infinite;
    border-left: 3px solid rgba(130,100,255,0.9);
}

/* ═══════════════════════════════════════════════════
   EMPTY STATE
═══════════════════════════════════════════════════ */
.empty-state {
    text-align: center;
    padding: 5rem 2rem;
    pointer-events: none;
}
.empty-state .bot-icon {
    font-size: 4rem;
    display: inline-block;
    animation: floatBob 3s ease-in-out infinite;
}
.empty-state h3 {
    margin: 0.8rem 0 0.3rem;
    font-size: 1.4rem;
    opacity: 0.75;
}
.empty-state p {
    opacity: 0.45;
    font-size: 0.95rem;
}

/* ═══════════════════════════════════════════════════
   TYPING INDICATOR (three bouncing dots)
═══════════════════════════════════════════════════ */
.typing-dots {
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 0.4rem 0.2rem;
}
.typing-dots span {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: rgba(130,100,255,0.8);
    animation: bounce 1.2s infinite ease-in-out;
}
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }

/* ═══════════════════════════════════════════════════
   FOOTER
═══════════════════════════════════════════════════ */
.footer {
    position: fixed;
    bottom: 3.8rem;
    right: 1.2rem;
    font-size: 0.7rem;
    opacity: 0.3;
    pointer-events: none;
    letter-spacing: 0.04em;
}
</style>
""", unsafe_allow_html=True)

# **************************************** utility functions *************************

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    # Check if messages key exists in state values, return empty list if not
    return state.values.get('messages', [])


# **************************************** Session Setup ******************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_thread(st.session_state['thread_id'])


# **************************************** Sidebar UI *********************************

with st.sidebar:
    st.markdown("## 🤖 LangGraph Chatbot")
    st.caption("Powered by LangGraph · Groq")
    st.divider()

    if st.button("＋  New Chat", use_container_width=True):
        reset_chat()

    st.markdown("#### 💬 My Conversations")

    all_threads = st.session_state['chat_threads'][::-1]
    total = len(all_threads)

    for i, thread_id in enumerate(all_threads):
        chat_number = total - i
        is_active = (thread_id == st.session_state['thread_id'])
        label = f"{'▶ ' if is_active else ''}Chat {chat_number}"

        if st.button(label, key=str(thread_id), use_container_width=True):
            st.session_state['thread_id'] = thread_id
            messages = load_conversation(thread_id)

            temp_messages = []

            for msg in messages:
                if isinstance(msg, HumanMessage):
                    role = 'user'
                else:
                    role = 'assistant'
                temp_messages.append({'role': role, 'content': msg.content})

            st.session_state['message_history'] = temp_messages


# **************************************** Main UI ************************************

st.markdown(
    '<p class="gradient-title">🤖 LangGraph Chatbot</p>',
    unsafe_allow_html=True,
)
st.caption(f"Thread: `{st.session_state['thread_id']}`")
st.divider()

# Animated empty state
if not st.session_state['message_history']:
    st.markdown(
        '<div class="empty-state">'
        '<span class="bot-icon">🤖</span>'
        '<h3>Start a conversation</h3>'
        '<p>Ask me anything — I am ready to help.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

user_input = st.chat_input('Type here...')

if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

    # Show typing indicator then stream response
    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        typing_placeholder.markdown(
            '<div class="typing-dots"><span></span><span></span><span></span></div>',
            unsafe_allow_html=True,
        )

        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"
            ):
                if isinstance(message_chunk, AIMessage):
                    # yield only assistant tokens
                    yield message_chunk.content

        typing_placeholder.empty()
        ai_message = st.write_stream(ai_only_stream())

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})

# Footer
st.markdown('<div class="footer">LangGraph · Groq · Streamlit</div>', unsafe_allow_html=True)