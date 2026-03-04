import streamlit as st
import re

st.set_page_config(page_title="Text Cleaner Tester", layout="wide")



def clean_spaces(text, mode):
    if mode == "Standard (စာပိုဒ်အလွတ် ၁ ကြောင်းချန်)":
        # စာကြောင်းအလွတ် ၃ ကြောင်းဆင့်နေရင် ၂ ကြောင်း (စာပိုဒ် ၁ ပိုဒ်စာ) ပဲ ချန်မယ်
        return re.sub(r'\n{3,}', '\n\n', text).strip()
    
    elif mode == "Compact (စာကြောင်းများ ကပ်ပစ်ရန်)":
        # စာကြောင်းအလွတ်အားလုံးကို ဖြုတ်ပြီး ၁ ကြောင်းချင်းစီ ကပ်ပစ်မယ်
        return re.sub(r'\n{2,}', '\n', text).strip()
    
    elif mode == "Ultimate (Space အားလုံးဖြုတ်ရန်)":
        # Double space တွေရော၊ စာကြောင်းအလွတ်တွေရော အကုန်ရှင်းမယ်
        temp = re.sub(r'\n+', '\n', text)
        return re.sub(r' +', ' ', temp).strip()
    
    return text

st.title("✂️ AI Text Space Cleaner Tester")
st.write("ဘယ်ဘက်မှာ Copy ကူးထည့်ပြီး ညာဘက်မှာ ရလဒ်ကို ကြည့်ပါ")

# Mode ရွေးချယ်ရန်
clean_mode = st.radio("သန့်ရှင်းရေးလုပ်မည့် ပုံစံ ရွေးပါ:", 
    ["Standard (စာပိုဒ်အလွတ် ၁ ကြောင်းချန်)", "Compact (စာကြောင်းများ ကပ်ပစ်ရန်)", "Ultimate (Space အားလုံးဖြုတ်ရန်)"])

col1, col2 = st.columns(2)

with col1:
    st.subheader("Original Result")
    raw_input = st.text_area("AI ဆီကစာသားကို ဒီမှာထည့်ပါ:", height=500)

with col2:
    st.subheader("Cleaned Result")
    if raw_input:
        cleaned_output = clean_spaces(raw_input, clean_mode)
        st.text_area("ရှင်းပြီးသားရလဒ်:", value=cleaned_output, height=500)
        st.code(cleaned_output) # Copy ကူးရလွယ်အောင် code block နဲ့ပါ ပြပေးထားသည်
    else:
        st.info("Input ထည့်ပေးဖို့ စောင့်နေပါတယ်။")

# app.py သို့ ပြန်သွားရန် Link
with st.sidebar:
    st.title("🔙 Navigation")
    main_app_url = "https://myanmar-ai-astrology-by-kyalngar.streamlit.app"
    st.link_button("🔮 Back to Main App", main_app_url, use_container_width=True)
