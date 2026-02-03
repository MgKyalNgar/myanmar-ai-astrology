import streamlit as st
import google.generativeai as genai
import os

# --- Page Config ---
st.set_page_config(page_title="Myanmar AI Astrology", page_icon="🔮", layout="centered")

# --- Custom CSS (Dark & Gold Theme) ---
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #D4AF37; }
    .stButton>button {
        background-color: #D4AF37; color: black; font-weight: bold; border-radius: 30px;
    }
    .result-card {
        background-color: #1E1E1E; padding: 20px; border-radius: 15px;
        border: 1px solid #D4AF37; color: #E0E0E0; line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🔮 မြန်မာ့အိပ်မက်အဘိဓာန် AI")

# API Key ခေါ်ယူခြင်း
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.5-flash')

    # User Input
    user_dream = st.text_area("သင်မက်ခဲ့တဲ့ အိပ်မက်ကို ပြောပြပါ...", placeholder="ဥပမာ - မြွေကြီးတစ်ကောင် မြင်မက်တယ်")

    if st.button("🔮 အဖြေရှာမယ်"):
        if user_dream:
            with st.spinner('နိမိတ်ဖတ်နေပါပြီ...'):
                try:
                    prompt = f"""
                    မင်းက မြန်မာ့ရိုးရာ အိပ်မက်နိမိတ်ဖတ် ပညာရှင်တစ်ယောက်ပါ။ 
                    အောက်ပါအိပ်မက်ကို မြန်မာလို အကျိုးအကြောင်းနဲ့တကွ ရှင်းပြပေးပါ။
                    
                    အိပ်မက်: {user_dream}
                    
                    ၁။ နိမိတ်အဓိပ္ပါယ် (ကောင်း/ဆိုး)
                    ၂။ အကျိုးပေးဂဏန်း (Lucky Numbers)
                    ၃။ ဆောင်ရန်/ရှောင်ရန် အကြံပြုချက်
                    
                    အဖြေကို ယဉ်ကျေးပျူငှာပြီး ယုံကြည်မှုရှိတဲ့ လေသံနဲ့ ဖြေပေးပါ။
                    """
                    response = model.generate_content(prompt)
                    st.markdown(f"<div class='result-card'>{response.text}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("အိပ်မက်တစ်ခုခု အရင်ရေးပေးပါဦး။")
else:
    st.error("API Key မတွေ့ပါ။ Settings ထဲမှာ အရင်ထည့်ပေးပါ။")