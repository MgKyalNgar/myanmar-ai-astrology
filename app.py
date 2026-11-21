import streamlit as st
from google import genai
from google.genai import types
import os
import datetime
import prompts
import streamlit.components.v1 as components

# --- Page Config ---
st.set_page_config(page_title="Myanmar AI Astrology", page_icon="🔮", layout="centered")

# --- PWA Mainframe Logic ---
# ဤ Code သည် Browser ကို Install လုပ်ရန် (Add to Home Screen) လှုံ့ဆော်ပေးပါလိမ့်မည်
st.markdown(f"""
    <link rel="manifest" href="manifest.json">
    <script>
    if ('serviceWorker' in navigator) {{
      window.addEventListener('load', function() {{
        navigator.serviceWorker.register('/sw.js').then(function(registration) {{
          console.log('ServiceWorker registration successful');
        }}, function(err) {{
          console.log('ServiceWorker registration failed: ', err);
        }});
      }});
    }}
    </script>
""", unsafe_allow_html=True)

# --- Offline Support Service Worker Logic ---
st.markdown("""
    <script>
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', function() {
        navigator.serviceWorker.register('./sw.js').then(function(reg) {
          console.log('Service Worker Registered!', reg);
        }).catch(function(err) {
          console.log('Service Worker Failed!', err);
        });
      });
    }
    </script>
""", unsafe_allow_html=True)

# --- Custom CSS (Particles & UI Fixes) ---
st.markdown("""
    <style>
    /* 1. Main App Background */
    .stApp {
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%) !important;
        overflow: hidden;
    }
    
    /* 2. Floating Stars Layer */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: transparent url('https://www.transparenttextures.com/patterns/stardust.png') repeat;
        background-size: 500px 500px;
        z-index: 0; /* Background layer */
        animation: move-stars 300s linear infinite; /* Star Speed */
        opacity: 0.6;
        pointer-events: none;
    }

    @keyframes move-stars {
        from { background-position: 0 0; }
        to { background-position: 10000px 5000px; }
    }

    /* 3. Content Visibility */
    .main .block-container {
        position: relative;
        z-index: 1; /* Content အားလုံးကို Stars ရဲ့ အပေါ်မှာထားခြင်း */
    }

    /* Light Mode မှာပါ စာသားတွေ အမြဲပေါ်နေအောင် Fixed လုပ်ခြင်း */
	/* Label စာသားများ (ဥပမာ - သင့်အမည်၊ အိပ်မက်ရေးပါ) */
	[data-testid="stWidgetLabel"] p, 
	label {
    	color: #D4AF37 !important; /* ရွှေရောင် */
    	font-weight: bold !important;
    	font-size: 1.1rem !important;
    	text-shadow: 1px 1px 2px black; /* စာလုံးပိုကြွလာအောင် */
	}

    .result-card {
        background-color: rgba(26, 28, 35, 0.95); 
        padding: 18px;
        border-radius: 15px;
        border: 1px solid #D4AF37; 
        color: #F0F0F0; 
        line-height: 1.4 !important; /* စာကြောင်း အကွာအဝေး */
        margin-top: 10px;          
        white-space: normal;    
        font-size: 1.05rem;        
    }

    .result-card h3, .result-card h4 {
        margin-top: 10px !important;
        margin-bottom: 5px !important;
        color: #D4AF37 !important;
        font-weight: bold !important;
    }

    /* List (အချက်အလက်ပြစာရင်း) များ၏ အကွာအဝေးကို ကျစ်လစ်စေခြင်း */
    .result-card ul {
        margin-top: 20px !important;
        margin-bottom: 20px !important;
        padding-left: 20px !important;
    }

    .result-card li {
        margin-bottom: 5px !important; /* အချက်တစ်ခုချင်းစီကြား အကွာအဝေး */
        line-height: 1.5 !important;
    }

        /* အလျားလိုက်မျဉ်း (hr) ထည့်ထားလျှင် အကွာအဝေးညှိရန် */
    .result-card hr {
        margin: 10px 0 !important;
        border: 0;
        border-top: 1px solid rgba(212, 175, 55, 0.3);
    }


    h1 { color: #D4AF37 !important; text-align: center; font-size: 2em !important; text-shadow: 2px 2px 4px #000; }

    /* Tabs Styling - ပိုကျယ်သွားအောင် ပြင်ထားသည် */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 55px; 
        background-color: rgba(26, 28, 35, 0.8); 
        border-radius: 10px 10px 0 0;
        color: white; 
        font-size: 16px;
        padding: 0 25px;
		border: 1px solid #D4AF37;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #D4AF37 !important; 
        color: black !important; 
        font-weight: bold;
    }

    .stButton>button {
        width: 100%; border-radius: 25px; height: 3.5em;
        background-color: #D4AF37; color: black; font-weight: bold; border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #FFD700; transform: scale(1.01); }
    </style>
    """, unsafe_allow_html=True)

# --- API Configuration ---
# အသုံးပြုမည့် Model များ (တစ်ခုကုန်လျှင် နောက်တစ်ခုပြောင်းရန်)
# 21 Nov 2026 စစ်ပြီး အလုပ်လုပ်ကြောင်း အတည်ပြုထားသော model များသာ
AVAILABLE_MODELS = [
    'gemini-3-flash-preview',
    'gemini-2.5-flash',
    'gemini-3.5-flash-lite'
]

api_key = os.getenv("GEMINI_API_KEY")
# New SDK (google-genai): client ကို key ရှိမှသာ ဆောက်မည်
client = None
if api_key:
    client = genai.Client(
        api_key=api_key,
        # v1beta — gemini-3-flash-preview က v1 မှာ မရှိသေးလို့ (21 Nov 2026 စစ်ပြီး)
        # StarFish လို တစ်ခေါက်ကို 60 စက္ကန့် timeout (milliseconds နဲ့ ရေးရသည်)
        http_options=types.HttpOptions(api_version="v1beta", timeout=60000)
    )
else:
    st.error("API Key Not Found Error")

# --- Lucky Color Logic ---
# မြန်မာစံတော်ချိန် (UTC+6:30) — Streamlit server က UTC သုံးလို့
MYANMAR_TZ = datetime.timezone(datetime.timedelta(hours=6, minutes=30))
now = datetime.datetime.now(MYANMAR_TZ)
today_myanmar = now.date()
day_name = now.strftime("%A") # ဥပမာ - Wednesday

lucky_data = {
    "Monday": {"color": "ဖြူစင်သော အဖြူရောင်", "hex": "#FFFFFF", "text": "တနင်္လာ"},
    "Tuesday": {"color": "တောက်ပသော အနီရောင်", "hex": "#FF0000", "text": "အင်္ဂါ"},
    "Wednesday": {"color": "စိမ်းလန်းသော အစိမ်းရောင်", "hex": "#00FF00", "text": "ဗုဒ္ဓဟူး/ရာဟု"},
    "Thursday": {"color": "ဝင်းပသော အဝါရောင်", "hex": "#FFFF00", "text": "ကြာသပတေး"},
    "Friday": {"color": "ကြည်လင်သော အပြာရောင်", "hex": "#0000FF", "text": "သောကြာ"},
    "Saturday": {"color": "နက်မှောင်သော ခရမ်းရောင်", "hex": "#800080", "text": "စနေ"},
    "Sunday": {"color": "ရွှေအိုရောင်/လိမ္မော်ရောင်", "hex": "#FFA500", "text": "တနင်္ဂနွေ"}
}

today_lucky = lucky_data.get(day_name, lucky_data["Monday"])

# --- Display Banner ---
st.markdown(f"""
    <div style="background-color: rgba(212, 175, 55, 0.1); border: 1px solid #D4AF37; padding: 10px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
        <span style="color: #D4AF37; font-size: 1.1rem;">✨ ယနေ့ <b>{today_lucky['text']}</b> နေ့အတွက် ကံကောင်းစေသောအရောင်မှာ <b style="color: {today_lucky['hex']}; text-shadow: 1px 1px 2px black;">{today_lucky['color']}</b> ဖြစ်ပါတယ် ✨</span>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h1>🔮 မြန်မာ့ဗေဒင်နှင့် ဓာတ်ရိုက်ဓာတ်ဆင် AI</h1>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["💞 အိမ်ထောင်ဖက်", "🌙 အိပ်မက်", "🛡️ ယတြာ", "✨ ဟောစာတမ်း", "📜 မဟာဘုတ်"])


# စာကြောင်းအလွတ် ၃ ကြောင်း သို့မဟုတ် ၃ ကြောင်းထက်ပိုပါက ၂ ကြောင်းသို့ လျှော့ချသည်
def clean_ai_text(text):
    import re
    cleaned_text = re.sub(r'\n{3,}', '\n', text)
    # စာကြောင်းတစ်ကြောင်းချင်းစီ၏ ရှေ့နှင့်နောက်မှ မလိုအပ်သော Space များကို ဖြုတ်သည်
    return cleaned_text

# --- Helper Function for AI ---
def get_ai_response(prompt, spinner_text="သင့်အတွက် တွက်ချက်နေပါသည်..."):
    loading_placeholder = st.empty()

    # API Key မရှိလျှင် ချက်ချင်း ရပ်ပါ
    if not api_key:
        st.error("API Key Not Found Error")
        return None

    with st.spinner(spinner_text):
        # ရနိုင်သမျှ Model တစ်ခုချင်းစီကို စမ်းကြည့်ခြင်း
        for model_name in AVAILABLE_MODELS:
            try:
                # လက်ရှိ loop ပတ်နေသော model ကို တည်ဆောက်သည်
                response = client.models.generate_content(
                    model=f'models/{model_name}',
                    contents=prompt
                )

                # အဖြေရလျှင် Clean လုပ်ပြီး ပြန်ပေးမည်
                final_text = clean_ai_text(response.text)
                return final_text

            except Exception as e:
                err = str(e)
                # New SDK က error code ကို .code attribute အဖြစ်ပါ ပေးသည်
                code = getattr(e, "code", None)
                # Key ပြဿနာ (401/403) ဆိုရင် နောက် model စမ်းလည်း အလကားဖြစ်လို့ ချက်ချင်း ရပ်ပါ
                if code in (401, 403) or "401" in err or "403" in err:
                    st.error(f"API Key Error ({model_name}): {err}")
                    return None
                # 429 (Token ကုန်), 404/400 (Model မရှိတော့တာ), 503/504 (Service မရတာ),
                # Timeout ဖြစ်ပါက နောက် model တစ်ခုကို ထပ်စမ်းမည်
                if code in (429, 404, 400, 503, 504) or any(c in err for c in ("429", "404", "400", "503", "504")) or "timed out" in err.lower() or "timeout" in err.lower():
                    continue  # နောက် Model သို့ ကျော်သွားရန်
                # အခြား Error ဖြစ်လျှင် ရပ်ပြီး အမှားပြမည်
                st.error(f"Error ({model_name}): {err}")
                return None

        # Model အားလုံး စမ်းပြီးလို့မှ မရခဲ့ရင်
        st.error("ရနိုင်သမျှ AI Model အားလုံး Token Limit ပြည့်သွားပါပြီ။ ခဏနားပြီးမှ ပြန်စမ်းပေးပါ။")
        return None
		

#  def get_ai_response(prompt, spinner_text):
#    loading_placeholder = st.empty()
#    try:
#        with st.spinner(spinner_text):
#            response = model.generate_content(prompt)
#            res_text = response.text
#            return res_text
#    except Exception as e:
#        loading_placeholder.empty()
#        if "429" in str(e):
#            st.error("AI Tokan Free Limit ပြည့်သွားပါပြီ။ ခဏနားပြီးမှ ပြန်စမ်းပေးပါ")
#        else:
#            st.error(f"Error တက်သွားပါတယ်: {str(e)}")
#        return None


# --- Tab 1: Compatibility (အိမ်ထောင်ဖက် ရွေးချယ်မှု) ---
with tab1:
    st.markdown("<p style='color: #D4AF37; font-size: 1.1rem; font-weight: bold;'>နှစ်ဦးသား လိုက်ဖက်ညီမှု စစ်ဆေးရန်</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("မိမိအချက်အလက်")
        u_name_comp = st.text_input("သင့်အမည်", key="u_comp")
        u_day_comp = st.selectbox("သင့်နေ့နံ", ["တနင်္ဂနွေ", "တနင်္လာ", "အင်္ဂါ", "ဗုဒ္ဓဟူး", "ရာဟု", "ကြာသပတေး", "သောကြာ", "စနေ"], key="u_day_comp")
        
    with col2:
        st.subheader("လက်တွဲဖော်")
        p_name_comp = st.text_input("လက်တွဲဖော်အမည်", key="p_comp")
        p_day_comp = st.selectbox("လက်တွဲဖော်နေ့နံ", ["တနင်္ဂနွေ", "တနင်္လာ", "အင်္ဂါ", "ဗုဒ္ဓဟူး", "ရာဟု", "ကြာသပတေး", "သောကြာ", "စနေ"], key="p_day_comp")

    if st.button("တွဲဖက်မှု စစ်ဆေးမယ် 💞"):
        if u_name_comp and p_name_comp:
            full_prompt = prompts.COMPATIBILITY_TEMPLATE.format(
                system_instruction=prompts.SYSTEM_INSTRUCTION,
                user_name=u_name_comp,
                user_day=u_day_comp,
                partner_name=p_name_comp,
                partner_day=p_day_comp
            )
            st.session_state['comp_res'] = get_ai_response(full_prompt, spinner_text="နှစ်ဦးသား လိုက်ဖက်မှုကို တွက်ချက်နေပါသည်...")
        else:
            st.warning("အမည်နှစ်ခုလုံးကို ပြည့်စုံအောင် ဖြည့်ပေးပါ ခင်ဗျာ။")

    # ရလဒ်ပြသခြင်း
    if 'comp_res' in st.session_state and st.session_state['comp_res']:
        st.markdown(f"<div class='result-card'>{st.session_state['comp_res']}</div>", unsafe_allow_html=True)
        st.download_button("📁 ရလဒ်ကိုသိမ်းမယ်", st.session_state['comp_res'], file_name="compatibility_result.txt")


# --- Tab 2: Dream ---
with tab2:
    user_dream = st.text_area("သင်မက်ခဲ့သည့် အိပ်မက်ကို ရေးပါ...", key="dream_input")
    if st.button("နိမိတ်ဖတ်မယ် 🌙"):
        if user_dream:
            full_prompt = prompts.DREAM_TEMPLATE.format(
                system_instruction=prompts.SYSTEM_INSTRUCTION,
                user_dream=user_dream
            )
            # Result ကို session state ထဲ သိမ်းသည်
            st.session_state['dream_res'] = get_ai_response(full_prompt)
        else:
            st.warning("အိပ်မက်ကို အရင်ရေးပေးပါ ခင်ဗျာ။")

    if 'dream_res' in st.session_state and st.session_state['dream_res']:
        st.markdown(f"<div class='result-card'>{st.session_state['dream_res']}</div>", unsafe_allow_html=True)
        st.download_button("📁 ရလဒ်ကိုသိမ်းမယ်", st.session_state['dream_res'], file_name="dream.txt")


# --- Tab 3: Yadaya ---
with tab3:
    u_name = st.text_input("သင့်အမည်")
     # ထပ်တိုးပေးထားသော အခက်အခဲများ
    prob = st.selectbox("ရင်ဆိုင်နေရသော အခက်အခဲ", [
            "စီးပွားရေးညံ့ခြင်း/ငွေကြေးခက်ခဲခြင်း", 
            "အချစ်ရေးအဆင်မပြေခြင်း", 
            "အိမ်ထောင်ရေးအဆင်မပြေခြင်း",
            "ကျန်းမာရေးမကောင်းခြင်း", 
            "အတိုက်အခံ/ရန်များခြင်း", 
            "အလုပ်အကိုင်ခက်ခဲခြင်း",
            "ပညာရေးအဆင်မပြေခြင်း",
            "အကြွေးကိစ္စအခက်အခဲဖြစ်ခြင်း",
            "တရားရင်ဆိုင်နေရခြင်း",
            "ခရီးသွားလာရန်အခက်အခဲရှိခြင်း"
    ])
    
    if st.button("ယတြာတောင်းမယ် 🛡️"):
        if u_name:
            full_prompt = prompts.YADAYA_TEMPLATE.format(
                system_instruction=prompts.SYSTEM_INSTRUCTION,
                user_name=u_name,
                problem=prob
            )
            st.session_state['yadaya_res'] = get_ai_response(full_prompt)
        else:
            st.warning("အမည် ထည့်ပေးပါ ခင်ဗျာ။")

    if 'yadaya_res' in st.session_state and st.session_state['yadaya_res']:
        st.markdown(f"<div class='result-card'>{st.session_state['yadaya_res']}</div>", unsafe_allow_html=True)
        st.download_button("📁 ယတြာကိုသိမ်းမယ်", st.session_state['yadaya_res'], file_name="yadaya.txt")

# --- Tab 4: Daily Horoscope ---
with tab4:
    day = st.selectbox("သင့်မွေးနေ့ ရွေးပါ", ["တနင်္ဂနွေ", "တနင်္လာ", "အင်္ဂါ", "ဗုဒ္ဓဟူး", "ရာဟု", "ကြာသပတေး", "သောကြာ", "စနေ"])
    if st.button("ဟောစာတမ်းကြည့်မယ် ✨"):
        full_prompt = prompts.HOROSCOPE_TEMPLATE.format(
            system_instruction=prompts.SYSTEM_INSTRUCTION,
            day=day,
            today=today_myanmar.strftime("%d %B %Y")
        )
        st.session_state['horo_res'] = get_ai_response(full_prompt)
            
    if 'horo_res' in st.session_state and st.session_state['horo_res']:
        st.markdown(f"<div class='result-card'>{st.session_state['horo_res']}</div>", unsafe_allow_html=True)
        st.download_button("📂 ဟောစာတမ်းသိမ်းမယ်", st.session_state['horo_res'], file_name="horoscope.txt")

# --- Tab 5: Mahabote (မဟာဘုတ် ဇာတာခွင်) ---
with tab5:
    st.markdown("<p style='color: #D4AF37; font-size: 1.1rem; font-weight: bold;'>သင့်မွေးသက္ကရာဇ်ကို ထည့်သွင်းပါ</p>", unsafe_allow_html=True)
    
    # Date Picker ထည့်ခြင်း
    dob = st.date_input("မွေးသက္ကရာဇ် (ခရစ်နှစ်)", value=today_myanmar, min_value=datetime.date(1920, 1, 1), max_value=today_myanmar)
    
    # နေ့နံ ရွေးချယ်ခြင်း (Tab 2 နဲ့ key မတူအောင် key="maha_day" ပေးထားသည်)
    birth_day = st.selectbox("မွေးဖွားရာ နေ့နံ", ["တနင်္ဂနွေ", "တနင်္လာ", "အင်္ဂါ", "ဗုဒ္ဓဟူး", "ရာဟု", "ကြာသပတေး", "သောကြာ", "စနေ"], key="maha_day")
    
    if st.button("ဇာတာတွက်မယ် 📜"):
        # မဟာဘုတ် အကြွင်းနှင့် အနေအထားကို code ထဲမှာ တွက်မည် (AI ကို တွက်ခိုင်းတော့မည် မဟုတ်ပါ)
        remainder = (dob.year - 638) % 7
        weekdays = ["တနင်္ဂနွေ", "တနင်္လာ", "အင်္ဂါ", "ဗုဒ္ဓဟူး", "ကြာသပတေး", "သောကြာ", "စနေ"]
        row0 = ["ပုတိ", "သိုက်", "မရဏ", "အဓိပတိ", "ရာဇ", "အထွန်း", "ဘင်္ဂ"]
        # ရာဟု သည် ဗုဒ္ဓဟူး နေ့လယ်ပိုင်း ဖြစ်လို့ ဇယားမှာ ဗုဒ္ဓဟူး ကော်လံပဲ သုံးမည်
        lookup_day = "ဗုဒ္ဓဟူး" if birth_day == "ရာဟု" else birth_day
        position = row0[(weekdays.index(lookup_day) - remainder) % 7]
        # ရွေးထားသော နေ့နံက မွေးနေ့နှင့် မကိုက်လျှင် သတိပေးမည် (ရွေးချယ်မှုကတော့ user အတိုင်း ဆက်သွားမည်)
        en_to_mm = {"Monday": "တနင်္လာ", "Tuesday": "အင်္ဂါ", "Wednesday": "ဗုဒ္ဓဟူး", "Thursday": "ကြာသပတေး", "Friday": "သောကြာ", "Saturday": "စနေ", "Sunday": "တနင်္ဂနွေ"}
        derived_day = en_to_mm[dob.strftime("%A")]
        if birth_day != derived_day and not (derived_day == "ဗုဒ္ဓဟူး" and birth_day == "ရာဟု"):
            st.warning(f"သတိပြုပါ — ရွေးထားသော နေ့နံ ({birth_day}) က မွေးသက္ကရာဇ်နှင့် မကိုက်ပါ။ {dob.strftime('%d %B %Y')} ရက်နေ့၏ နေ့နံမှာ {derived_day} ဖြစ်ပါသည်။")
        full_prompt = prompts.MAHABOTE_TEMPLATE.format(
            system_instruction=prompts.SYSTEM_INSTRUCTION,
            dob=dob.strftime("%Y-%m-%d"),
            day=birth_day,
            remainder=remainder,
            position=position
        )
        st.session_state['mahabote_res'] = get_ai_response(full_prompt, spinner_text="မဟာဘုတ်ခွင် တွက်ချက်နေပါသည်...")

    # ရလဒ်ပြသခြင်း
    if 'mahabote_res' in st.session_state and st.session_state['mahabote_res']:
        st.markdown(f"<div class='result-card'>{st.session_state['mahabote_res']}</div>", unsafe_allow_html=True)
        st.download_button("📁 ဇာတာကိုသိမ်းမယ်", st.session_state['mahabote_res'], file_name="mahabote_astrology.txt")

        
# --- Viewer Counter & Facebook Share Section ---
# --- Footer Section (Revised Version) ---
st.divider()

# Link အမှန်ကို သတ်မှတ်ခြင်း
app_url_official = "https://myanmar-ai-astrology-by-kyalngar.streamlit.app"

# အခြား Counter တစ်ခု (VisitorBadge.io) ကို ပြောင်းသုံးကြည့်ပါမည်
# ဒါက hits ထက်စာရင် broken link ဖြစ်နိုင်ခြေ ပိုနည်းပါသည်
counter_html_new = f"""
<div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
    <div style="color: #D4AF37; font-size: 0.9rem; font-weight: bold;">
        Developed with ❤️ by Mg Kyal Ngar | Astrology AI v3.5
    </div>
    <div>
        <a href="https://visitorbadge.io/status?path={app_url_official}">
            <img src="https://api.visitorbadge.io/api/combined?path={app_url_official}&label=VISITORS&countColor=%23d4af37&style=flat" alt="Visitor Counter"/>
        </a>
    </div>
</div>
"""
st.markdown(counter_html_new, unsafe_allow_html=True)

# Facebook Share Button
st.markdown(f"""
    <div style="text-align: center; margin-top: 25px;">
        <a href="https://www.facebook.com/sharer/sharer.php?u={app_url_official}" target="_blank" style="text-decoration: none;">
            <div style="background-color: #1877F2; color: white; padding: 10px 25px; border-radius: 25px; font-weight: bold; display: inline-block;">
                🔵 Facebook မှာ Share မယ်
            </div>
        </a>
    </div>
""", unsafe_allow_html=True)

