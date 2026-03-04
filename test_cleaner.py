import streamlit as st
import re

def clean_ai_text(text):
    # ၁။ စာကြောင်းအစနှင့် အဆုံးရှိ space များကို ဖြုတ်သည်
    # ၂။ စာကြောင်းအလွတ် ၃ ကြောင်းဆင့်နေပါက ၂ ကြောင်းသို့ လျှော့သည်
    # ၃။ စာကြောင်းတစ်ကြောင်းချင်းစီ၏ ဝဲ/ယာ space များကို ရှင်းသည်
    temp_text = re.sub(r'\n{3,}', '\n\n', text)
    cleaned_lines = [line.strip() for line in temp_text.split('\n')]
    return '\n'.join(cleaned_lines)

st.title("✂️ AI Text Space Cleaner Tester")
st.write("AI ဆီကရတဲ့ စာသားတွေကို ဘယ်ဘက်အကွက်မှာ ထည့်ပြီး စမ်းကြည့်ပါ")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Original Result (AI ဆီကစာသား)")
    input_text = st.text_area("ဒီမှာ Copy ကူးထည့်ပါ", height=400, placeholder="စာသားများကို ဤနေရာတွင် ထည့်ပါ...")

with col2:
    st.subheader("Cleaned Result (ရှင်းပြီးသား)")
    if input_text:
        processed_text = clean_ai_text(input_text)
        st.text_area("Space ဖြုတ်ပြီးရလဒ်", value=processed_text, height=400, key="output_text")
    else:
        st.info("ဘယ်ဘက်တွင် စာသားထည့်ပါက ဤနေရာတွင် အလိုအလျောက် ရှင်းပေးပါမည်။")

if st.button("Clean Space Again 🧹"):
    st.rerun()

st.divider()
st.markdown("""
**ရှင်းလင်းချက်:**
* အကယ်၍ စာကြောင်းတွေကြားမှာ `\n` အပိုတွေ အရမ်းများနေရင် `re.sub(r'\n{2,}', '\n', text)` လို့ ပြောင်းသုံးကြည့်ပါ။ 
* ဒါဆိုရင် စာကြောင်းတွေ အကုန်လုံး ကပ်သွားပါလိမ့်မယ်။
""")
