import streamlit as st
import re

st.set_page_config(page_title="Text Cleaner Tester", layout="wide")

def clean_spaces(text, mode):
    if mode == "Standard (စာပိုဒ်အလွတ် ၁ ကြောင်းချန်)":
        # စာကြောင်း ၃ ကြောင်းဆင့်နေရင် ၂ ကြောင်းပဲ ချန်မယ် (စာပိုဒ် ခွဲရုံပဲ)
        return re.sub(r'\n{3,}', '\n\n', text).strip()
    
    elif mode == "Compact (စာကြောင်းများ ကပ်ပစ်ရန်)":
        # စာကြောင်းအလွတ် (Blank Lines) တွေအားလုံးကို ဖြုတ်ပစ်မယ်
        # \n\n တွေကို \n တစ်ခုတည်း ဖြစ်အောင် ပြောင်းတာပါ
        temp = re.sub(r'\n\s*\n', '\n', text)
        return temp.strip()
    
    elif mode == "Ultimate (Space အားလုံးဖြုတ်ရန်)":
        # ၁။ စာကြောင်းအလွတ်တွေ အကုန်ဖြုတ်မယ်
        temp = re.sub(r'\n\s*\n', '\n', text)
        # ၂။ စာကြောင်းတစ်ကြောင်းချင်းစီရဲ့ ရှေ့နဲ့နောက်က space တွေကို ဖြုတ်မယ်
        lines = [line.strip() for line in temp.split('\n')]
        temp = '\n'.join(lines)
        # ၃။ စာသားတွေကြားထဲမှာ space ၂ ခု (သို့) ၂ ခုထက်ပိုပါနေရင် ၁ ခုတည်း ဖြစ်အောင်လုပ်မယ်
        # ဥပမာ - "မင်္ဂလာ  ပါ" ကို "မင်္ဂလာ ပါ" ဖြစ်အောင် ပြောင်းတာပါ
        final = re.sub(r' +', ' ', temp)
        return final.strip()
    
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
