import streamlit as st
import google.generativeai as genai
import os

# --- Page Config ---
st.set_page_config(page_title="Myanmar AI Astrology", page_icon="🔮", layout="centered")

# --- Custom CSS (Dark Mode, Gold Theme & Animated Background) ---
st.markdown("""
    <style>
    /* Background Animation */
    .stApp {
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%);
        color: #E0E0E0;
    }
    
    /* စာပိုဒ်ကျဲနေတာကို ပြင်ရန် */
    .result-card {
        background-color: rgba(26, 28, 35, 0.8); 
        padding: 20px; 
        border-radius: 15px;
        border: 1px solid #D4AF37; 
        color: #E0E0E0; 
        line-height: 1.5; /* စာကြောင်းအကွာအဝေးကို လျှော့ချထားသည် */
        margin-top: 10px;
        white-space: pre-wrap;
    }
    
    /* Paragraph spacing ပြင်ဆင်ခြင်း */
    .result-card p {
        margin-bottom: 8px !important;
    }

    h1, h2, h3 { color: #D4AF37 !important; text-align: center; }

    .stButton>button {
        width: 100%; border-radius: 25px; height: 3em;
        background-color: #D4AF37; color: black; font-weight: bold; border: none;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        height: 45px; background-color: #1A1C23; border-radius: 10px 10px 0 0;
        color: white; font-size: 14px;
    }
    .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# --- API Configuration ---
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
else:
    st.error("API Key မတွေ့ပါ။ Settings ထဲမှာ GEMINI_API_KEY ထည့်ပေးပါ။")

st.markdown("<h1>🔮 မြန်မာ့ဗေဒင်နှင့် ဓာတ်ရိုက်ဓာတ်ဆင် AI</h1>", unsafe_allow_html=True)

# --- AI Personality & Grammar Logic ---
# နာမည်ရှေ့မှာ ခင်ဗျာ မပါစေရန်နှင့် စာကြောင်းအကွာအဝေး ကျစ်လျစ်စေရန် ညွှန်ကြားချက်
system_instruction = """
မင်းက မြန်မာ့ရိုးရာ ဗေဒင်ပညာရှင် ယောကျ်ားလေးတစ်ယောက်ပါ။ 
စကားပြောရင် 'ကျွန်တော်' နဲ့ 'ခင်ဗျာ' ကို သုံးရပါမယ်။ 
အရေးကြီးသောအချက် - တစ်ဖက်လူကို နှုတ်ဆက်တဲ့အခါ 'မင်္ဂလာပါ [နာမည်] ခင်ဗျာ' လို့ပဲ သုံးပါ။ 'မင်္ဂလာပါ ခင်ဗျာ [နာမည်]' လို့ မပြောပါနဲ့။
အဖြေတွေကို ရေးတဲ့အခါ စာကြောင်းတွေကြားမှာ space အလွတ်တွေ အများကြီး မခြားပါနဲ့။ ကျစ်ကျစ်လျစ်လျစ်နဲ့ ဖတ်ရလွယ်အောင် ရေးပေးပါ။
"""

tab1, tab2, tab3 = st.tabs(["🌙 အိပ်မက်", "✨ ဟောစာတမ်း", "🛡️ ယတြာ"])

# --- Tab 1: Dream ---
with tab1:
    user_dream = st.text_area("သင်မက်ခဲ့သည့် အိပ်မက်ကို ရေးပါ...", height=100)
    if st.button("နိမိတ်ဖတ်မယ်"):
        if user_dream:
            with st.spinner('ကျွန်တော် တွက်ချက်ပေးနေပါတယ် ခင်ဗျာ...'):
                prompt = f"{system_instruction} အိပ်မက်: '{user_dream}' ကို နိမိတ်ဖတ်ပေးပါ။"
                response = model.generate_content(prompt)
                st.markdown(f"<div class='result-card'>{response.text}</div>", unsafe_allow_html=True)

# --- Tab 2: Daily Horoscope ---
with tab2:
    day = st.selectbox("သင့်မွေးနေ့ (နေ့နံ) ရွေးပါ", ["တနင်္ဂနွေ", "တနင်္လာ", "အင်္ဂါ", "ဗုဒ္ဓဟူး", "ရာဟု", "ကြာသပတေး", "သောကြာ", "စနေ"])
    if st.button("ဟောစာတမ်းကြည့်မယ်"):
        with st.spinner('နက္ခတ်ကို ကြည့်ပေးနေပါတယ် ခင်ဗျာ...'):
            prompt = f"{system_instruction} {day} သားသမီးတွေအတွက် ဒီနေ့အတွက် ဟောစာတမ်းကို ရှင်းပြပေးပါ။"
            response = model.generate_content(prompt)
            st.markdown(f"<div class='result-card'>{response.text}</div>", unsafe_allow_html=True)

# --- Tab 3: Yadaya ---
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("သင့်အမည်")
    with col2:
        problem = st.selectbox("ရင်ဆိုင်နေရသော အခက်အခဲ", ["စီးပွားရေးညံ့ခြင်း", "အချစ်ရေးအဆင်မပြေခြင်း", "ကျန်းမာရေးမကောင်းခြင်း", "အတိုက်အခံများခြင်း", "အလုပ်အကိုင်ခက်ခဲခြင်း"])
    
    if st.button("ယတြာတောင်းမယ်"):
        if user_name:
            with st.spinner('ယတြာတွက်ချက်ပေးနေပါတယ် ခင်ဗျာ...'):
                # နာမည်နဲ့ နှုတ်ဆက်ပုံကို Prompt မှာ အသေသတ်မှတ်ပေးလိုက်ခြင်း
                prompt = f"{system_instruction} အမည် {user_name} က {problem} ဖြစ်နေတာအတွက် ယတြာပေးပါ။ အစမှာ 'မင်္ဂလာပါ {user_name} ခင်ဗျာ' လို့ပဲ နှုတ်ဆက်ပါ။"
                response = model.generate_content(prompt)
                st.markdown(f"<div class='result-card'>{response.text}</div>", unsafe_allow_html=True)
        else:
            st.warning("အမည် ထည့်ပေးပါ ခင်ဗျာ။")

st.divider()
st.caption("Developed with ❤️ by Mg Kyal Ngar | Astrology AI")
