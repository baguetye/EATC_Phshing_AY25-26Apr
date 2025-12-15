


import streamlit as st
import joblib
import pandas as pd
import time



st.set_page_config(layout="wide")
# --- Load model ---
model = joblib.load("rf_phishing_model_10-updated.pkl")
# --- Features and questions ---
features = [
    'UsingIP', 'LongURL', 'ShortURL', 'Symbol@', 'Redirecting//',
    'PrefixSuffix-', 'SubDomains', 'HTTPS',
    'NonStdPort', 'AbnormalURL'
]

feature_question_map = {
    'UsingIP': 'Does the URL use an IP address instead of a domain name?',
    'LongURL': 'Is the URL unusually long?',
    'ShortURL': 'Is the URL shortened (e.g., bit.ly)?',
    'Symbol@': 'Does the URL contain the "@" symbol?',
    'Redirecting//': 'Does the URL contain multiple "//" redirects?',
    'PrefixSuffix-': 'Does the domain name contain a "-" (prefix/suffix)?',
    'SubDomains': 'Are there many subdomains in the URL?',
    'HTTPS': 'Does the site use HTTPS (SSL certificate)?',
    'NonStdPort': 'Is the website using a non-standard port?',
    'AbnormalURL': 'Is the URL structure abnormal or inconsistent?'
}



feature_image_map = {
    'UsingIP': 'images/UsingIP.png',
    'LongURL': 'images/LongURL.png',
    'ShortURL': 'images/ShortURL.png',
    'Symbol@': 'images/SymbolAt.png',
    'Redirecting//': 'images/Redirecting.png',
    'PrefixSuffix-': 'images/PrefixSuffix.png',
    'SubDomains': 'images/SubDomains.png',
    'HTTPS': 'images/HTTPS.png',
    'NonStdPort': 'images/Non-Standard-Ports.png',
    'AbnormalURL': 'images/abnormalURL.png'
}

feature_captions_map = {
    'UsingIP': 'Fig. 1 – URL uses an IP address instead of a domain name.',
    'LongURL': 'Fig. 2 – Suspiciously long web address, often used to hide the real domain.',
    'ShortURL': 'Fig. 3 – Shortened link (e.g., bit.ly) hides the real destination.',
    'Symbol@': 'Fig. 4 – URL contains the “@” symbol, which can mislead users about the actual destination.',
    'Redirecting//': 'Fig. 5 – Multiple redirects before reaching the final page.',
    'PrefixSuffix-': 'Fig. 6 – Domain name includes a dash (“-”) to mimic a legitimate site.',
    'SubDomains': 'Fig. 7 – Multiple subdomains make the URL look similar to a trusted site.',
    'HTTPS': 'Fig. 8 – Website without HTTPS (secure connection) — a red flag for sensitive transactions.',
    'NonStdPort': 'Fig. 11 – Site uses uncommon network ports, possibly to bypass security.',
    'AbnormalURL': 'Fig. 18 – URL structure is abnormal compared to legitimate sites.'
}
feature_tips_map = {
    'UsingIP': 'Check if the URL starts with numbers (e.g., 192.168...).',
    'LongURL': 'Hover over the link — long or random URLs can be suspicious.',
    'ShortURL': 'Use a URL expander to reveal the real address.',
    'Symbol@': 'Look for “@” — only what’s after it matters.',
    'Redirecting//': 'Watch for multiple “//” in the link path.',
    'PrefixSuffix-': 'Look for dashes in the domain name.',
    'SubDomains': 'Count the dots — too many means likely fake.',
    'HTTPS': 'Check for the padlock icon or HTTPS in the bar.',
    'NonStdPort': 'Look for “:8080” or odd ports in the URL.',
    'AbnormalURL': 'Compare layout to the real site’s URL.'
}





value_labels = {-1: "🔴 No", 0: "🟡 Not Sure", 1: "🟢 Yes"}
value_options = [-1, 0, 1]

st.markdown("""
<style>
[data-testid="stImage"] {
  /* Your CSS styles go here */
  display:block;
  margin-left: auto;
  margin-right: auto;
  margin-bottom:10px;
  border: 4px solid #005C9F;;
  border-radius:20px;

}</style>
""", unsafe_allow_html=True)


# Embed the font link
with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


if "submitted" not in st.session_state:
    st.session_state.submitted = False

if not st.session_state.submitted:
    # --- Session state ---
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {}

    st.markdown("""
    <div class="header-container">
        <h1>AI Phishing Website Detection Questionnaire</h1>
        
    </div>
    """, unsafe_allow_html=True)
    
    progress = (st.session_state.current_index + 1) / len(features)
    
    half1, half2 ,half3 , half4 = st.columns([0.6,1.3,2,0.7],gap="small",vertical_alignment="center")
   
    with half3:
        with st.container(height=730,border=True):
            # --- Current question ---
            idx = st.session_state.current_index
            feature = features[idx]
            question = feature_question_map[feature]


            st.subheader(f"Question {idx + 1} of {len(features)}")

            # Show image if available
            if feature in feature_image_map:
                st.image(feature_image_map[feature], caption=feature_captions_map[feature],width=710)

            # Determine saved or default value
            default_val = st.session_state.answers.get(feature, 0)
            default_idx = value_options.index(default_val) if default_val in value_options else 1

            
            st.markdown(
                f"<p style='font-size:25px; color:var(--text-color); font-weight:500; margin-bottom:0px; margin-top:0px;'>{question}</p>",
                unsafe_allow_html=True
            )


            # --- User input ---
            answer = st.radio(
                label="",
                options=value_options,
                format_func=lambda x: value_labels[x],
                index=default_idx,
                key=f"radio_{feature}"
            )


            # 3. Add a submit button inside the form

            col1, col2, col3 = st.columns([3, 4, 3])

            with col1:
                if idx > 0 and st.button("⬅️ Back"):
                    st.session_state.current_index -= 1
                    st.session_state.answers[feature] = answer
                    st.rerun()


            with col3:
                if idx < len(features) - 1 and st.button("➡️ Next"):
                    st.session_state.current_index += 1
                    st.session_state.answers[feature] = answer
                    st.rerun()


            # --- Inside col3: Just the button ---
            with col3:
                submit_clicked = False
                if idx == len(features) - 1:
                    submit_clicked = st.button("🔍 Submit & Predict")
                    if submit_clicked:
                        st.session_state.answers[feature] = answer
                        st.session_state.submitted = True

                        st.rerun()



    with half2:
        import base64
        file_ = open("images/Robot-Bot 3D.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
        with st.container(height=730, border=True):
            if idx == 0:
                st.subheader(f"{10} questions more to go!")
            elif idx == 8:
                st.subheader(f"1 more question to go!")
            elif idx == 9:
                st.subheader(f"Last question!")
            else:

                st.subheader(f"{10-(idx+1)} questions more to go!")
            
            st.markdown(
                f'<img src="data:image/gif;base64,{data_url}" alt="cat gif" class="my-image">',
                unsafe_allow_html=True,
            )

           
            st.progress(progress, text=f"{int(progress * 100)}% completed")
           
            st.markdown(
                f"<p class='tip-text' style='font-size:28px; color:var(--text-color); font-weight:500; margin-bottom:0px; margin-top:10px;'><span style='color:#005C9F; font-weight:bold;'>Tip</span>:&nbsp;{feature_tips_map[feature]}</p>",
                unsafe_allow_html=True
            )

            with st.spinner("Analysing response...", width=500):
                time.sleep(1)










# --- Outside the columns: Handle prediction and display results in full width ---
else:

    import base64
    file_ = open("images/Hacker.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    file_ = open("images/Security.gif", "rb")
    contents = file_.read()
    data_url2 = base64.b64encode(contents).decode("utf-8")
    file_.close()

    input_values = [st.session_state.answers.get(f, 0) for f in features]
    prediction = model.predict([input_values])[0]

    st.markdown("""
           <div class="header-container">
               <h1>AI Phishing Website Detection Questionnaire</h1>
               
           </div>
           """, unsafe_allow_html=True)
   
    half1, half2, half3, half4 = st.columns([0.6, 1.3, 2, 0.7], gap="small", vertical_alignment="center")

    with half2:
        with st.container(height=650, border=True):
            st.subheader("📝 Your Responses")
            responses = {
                "Questions": [feature_question_map[f] for f in features],
                "Answer": [value_labels[st.session_state.answers.get(f, 0)] for f in features]
            }

            df_responses = pd.DataFrame(responses)

            st.dataframe(df_responses, use_container_width=True, hide_index=True)

            if st.button("🔄 Restart Questionnaire"):
                st.session_state.submitted = False
                st.session_state.current_index = 0
                st.session_state.answers = {}
                st.rerun()




    with half3:

        

        # 🔻 FULL WIDTH STYLED PREDICTION BOX
        with st.container(height=650, border=True):
            st.subheader("🎯 Prediction Result")
            if prediction == -1:
                st.markdown(
                    f"""
                        <div style='background-color:#d4edda; color:#155724; padding:1rem; border-radius:10px; font-size:35px; width:100%; text-align:center; margin-bottom:20px;'>
                            ✅ Website is <strong>LEGITIMATE</strong>
                        </div>
                        """,
                    unsafe_allow_html=True
                )
                st.markdown(
                    f'<img src="data:image/gif;base64,{data_url2}" alt="cat gif" class="my-image2">',
                    unsafe_allow_html=True,
                )

            else:
                st.markdown(
                    f"""
                        <div style='background-color:#f8d7da; color:#721c24; padding:1rem; border-radius:10px; font-size:35px; width:100%; text-align:center; margin-bottom:20px;'>
                            🚨 Website is <strong>PHISHING</strong>
                        </div>
                        """,
                    unsafe_allow_html=True
                )
                st.markdown(
                    f'<img src="data:image/gif;base64,{data_url}" alt="cat gif" class="my-image">',
                    unsafe_allow_html=True,
                )

        # --- Feature Importance ---









# In[ ]:





