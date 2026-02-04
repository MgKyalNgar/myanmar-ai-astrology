import streamlit as st
import google.generativeai as genai
import os
import re

# --- Page Config ---
st.set_page_config(page_title="Myanmar AI Astrology", page_icon="🔮", layout="centered")

# --- Custom CSS (Dark Mode & Gold Theme) ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    h1, h2, h3 { color: #D4AF37 !important; text-align: center; }
    
    .stButton>button {
        width: 100%; border-radius: 25px; height: 3em;
        background-color: #D4AF37; color: black; font-weight: bold; border: none;
    }
    .stButton>button:hover { background-color: #FFD700; color: black; }
    
    .result-card {
        background-color: #1A1C23; padding: 20px; border-radius: 15px;
        border: 1px solid #D4AF37; color: #E0E0E0; line-height: 1.8;
        margin-top: 20px; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.1);
    }
    
    /* Tab color customization */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; background-color: #1A1C23; border-radius: 10px 10px 0 0;
        color: white; padding: 0 20px;
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
    st.error("API Key မတွေ့ပါ။ Advanced Settings ထဲက Secrets မှာ GEMINI_API_KEY ထည့်ပေးပါ။")

st.markdown("<h1>🔮 မြန်မာ့အိပ်မက်နှင့် ဗေဒင် AI</h1>", unsafe_allow_html=True)

# --- Tabs for Features ---
tab1, tab2 = st.tabs(["🌙 အိပ်မက်အဘိဓာန်", "✨ နေ့စဉ်ဟောစာတမ်း"])

# --- Tab 1: Dream Interpreter ---
with tab1:
    st.markdown("### သင်မက်ခဲ့တဲ့ အိပ်မက်ကို ပြောပြပါ")
    user_dream = st.text_area("အိပ်မက်အကျဉ်းချုပ်...", height=100, key="dream_input")
    
    if st.button("နိမိတ်ဖတ်မယ် 🌙"):
        if user_dream:
            with st.spinner('AI ပညာရှင်က နိမိတ်ဖတ်ပေးနေပါတယ်...'):
                try:
                    prompt = f"မင်းက မြန်မာ့ရိုးရာ အိပ်မက်နိမိတ်ဖတ် ပညာရှင်တစ်ယောက်ပါ။ '{user_dream}' ဆိုတဲ့ အိပ်မက်ကို မြန်မာလို နိမိတ်ဖတ်ပေးပါ။ အကျိုးပေးဂဏန်း၊ ကောင်းဆိုးနိမိတ်နဲ့ ဆောင်ရန်ရှောင်ရန်တွေကို Sassy မဟုတ်ဘဲ လေးလေးနက်နက်နဲ့ ယုံကြည်ချင်စရာကောင်းအောင် ဖြေပေးပါ။"
                    response = model.generate_content(prompt)
                    st.markdown(f"<div class='result-card'>{response.text}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("အိပ်မက်အရင်ရေးပေးပါ။")

# --- Tab 2: Daily Horoscope ---
with tab2:
    st.markdown("### သင့်ရဲ့ မွေးနေ့ကို ရွေးချယ်ပါ")
    day = st.selectbox("နေ့နံ ရွေးရန်", ["တနင်္ဂနွေ", "တနင်္လာ", "အင်္ဂါ", "ဗုဒ္ဓဟူး", "ရာဟု", "ကြာသပတေး", "သောကြာ", "စနေ"])
    
    if st.button("ဟောစာတမ်းကြည့်မယ် ✨"):
        with st.spinner('ကံကြမ္မာကို တွက်ချက်နေပါတယ်...'):
            try:
                prompt = f"မင်းက မြန်မာ့ရိုးရာ ဗေဒင်ပညာရှင်ပါ။ {day} သားသမီးတွေအတွက် ဒီနေ့အတွက် ဟောစာတမ်းကို မြန်မာလို ဟောပေးပါ။ အချစ်ရေး၊ လူမှုရေး၊ စီးပွားရေးနဲ့ ကံကောင်းစေမယ့် အရောင်၊ ဂဏန်းတွေကို အသေးစိတ် ထည့်သွင်းပေးပါ။"
                response = model.generate_content(prompt)
                st.markdown(f"<div class='result-card'>{response.text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.divider()
st.caption("Developed with ❤️ by Mg Kyal Ngar | GitHub & Streamlit")
