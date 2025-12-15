


import streamlit as st
import joblib
import pandas as pd
import time




st.set_page_config(layout="wide")
# --- Load model ---
model = joblib.load("rf_phishing_model_10.pkl")
# --- Features and questions ---
features = [
        
    'PrefixSuffix-', 'SubDomains', 'HTTPS', 'DomainRegLen', 'RequestURL', 'AnchorURL',
    'LinksInScriptTags', 'ServerFormHandler', 
    'WebsiteTraffic',
    'LinksPointingToPage'
]

feature_question_map = {
    'PrefixSuffix-': 'Does the domain name contain a "-" (prefix/suffix)?',
    'SubDomains': 'Are there many subdomains in the URL?',
    'HTTPS': 'Does the site use HTTPS (SSL certificate)?',
    'DomainRegLen': 'Is the domain registered for a long period?',
    'RequestURL': 'Are images/scripts loaded from external URLs?',
    'AnchorURL': 'Do most anchor tags point to different domains?',
    'LinksInScriptTags': 'Are there links inside &lt;script&gt; tags?',
    'ServerFormHandler': 'Is form data sent to a suspicious domain?',
    'WebsiteTraffic': 'Does the site have high traffic?',
    'LinksPointingToPage': 'Are there many links pointing to this page?'
}



feature_image_map = {
    'PrefixSuffix-': 'images/PrefixSuffix.png',
    'SubDomains': 'images/SubDomains.png',
    'HTTPS': 'images/HTTPS.png',
    'DomainRegLen': 'images/DomainRegLen.png',
    'RequestURL': 'images/requesturl.png',
    'AnchorURL': 'images/AnchorURL.png',
    'LinksInScriptTags': 'images/LinksInScriptTags.png',
    'ServerFormHandler': 'images/formhandler.jpg',
    'WebsiteTraffic': 'images/WebTraffic.jpg',
    'LinksPointingToPage': 'images/LinksToPage.png'
}

feature_captions_map = {
    'PrefixSuffix-': 'Fig. 6 – Domain name includes a dash (“-”) to mimic a legitimate site.',
    'SubDomains': 'Fig. 7 – Multiple subdomains make the URL look similar to a trusted site.',
    'HTTPS': 'Fig. 8 – Website without HTTPS (secure connection) — a red flag for sensitive transactions.',
    'DomainRegLen': 'Fig. 9 – Recently registered domain, often used in phishing.',
    'RequestURL': 'Fig. 13 – Page loads resources from suspicious external domains.',
    'AnchorURL': 'Fig. 14 – Many anchor tags pointing to unrelated or malicious websites.',
    'LinksInScriptTags': 'Fig. 15 – Links hidden inside <script> code to load malicious content.',
    'ServerFormHandler': 'Fig. 16 – Form submission handler points to an untrusted server.',
    'WebsiteTraffic': 'Fig. 26 – Low or suspicious website traffic',
    'LinksPointingToPage': 'Fig. 29 – Few or no inbound links to the site'
}
feature_tips_map = {
    'PrefixSuffix-': 'Look for dashes in the domain name.',
    'SubDomains': 'Count the dots — too many means likely fake.',
    'HTTPS': 'Check for the padlock icon or HTTPS in the bar.',
    'DomainRegLen': 'Use WHOIS to see when the domain was made.',
    'RequestURL': 'Check if images/scripts load from odd sites.',
    'AnchorURL': 'Hover links — unrelated sites are a warning.',
    'LinksInScriptTags': 'View source for scripts from odd domains.',
    'ServerFormHandler': 'Hover “Submit” to see where data goes.',
    'WebsiteTraffic': 'Check traffic via SimilarWeb or Alexa.',
    'LinksPointingToPage': 'Check backlinks with online tools.'
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
                st.subheader(f"Last question to go!")
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






