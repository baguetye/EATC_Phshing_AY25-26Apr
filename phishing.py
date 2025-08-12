


import streamlit as st
import joblib
import pandas as pd

# --- Load model ---
model = joblib.load("rf_phishing_model.pkl")
# --- Features and questions ---
features = [
    'UsingIP', 'LongURL', 'ShortURL', 'Symbol@', 'Redirecting//',
    'PrefixSuffix-', 'SubDomains', 'HTTPS', 'DomainRegLen', 'Favicon',
    'NonStdPort', 'HTTPSDomainURL', 'RequestURL', 'AnchorURL',
    'LinksInScriptTags', 'ServerFormHandler', 'InfoEmail', 'AbnormalURL',
    'WebsiteForwarding', 'StatusBarCust', 'DisableRightClick',
    'UsingPopupWindow', 'IframeRedirection', 'AgeofDomain',
    'DNSRecording', 'WebsiteTraffic', 'PageRank', 'GoogleIndex',
    'LinksPointingToPage', 'StatsReport'
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
    'DomainRegLen': 'Is the domain registered for a long period?',
    'Favicon': 'Is the favicon loaded from a different domain?',
    'NonStdPort': 'Is the website using a non-standard port?',
    'HTTPSDomainURL': 'Does "HTTPS" appear in the domain name?',
    'RequestURL': 'Are images/scripts loaded from external URLs?',
    'AnchorURL': 'Do most anchor tags point to different domains?',
    'LinksInScriptTags': 'Are there links inside &lt;script&gt; tags?',
    'ServerFormHandler': 'Is form data sent to a suspicious domain?',
    'InfoEmail': 'Is an email address found in the domain’s WHOIS information?',
    'AbnormalURL': 'Is the URL structure abnormal or inconsistent?',
    'WebsiteForwarding': 'Does the site redirect the user multiple times?',
    'StatusBarCust': 'Is the status bar customized by JavaScript?',
    'DisableRightClick': 'Is right-click disabled?',
    'UsingPopupWindow': 'Does the site use popup windows?',
    'IframeRedirection': 'Does the site use &lt;iframe&gt; redirection?',
    'AgeofDomain': 'Is the domain very new or recently registered?',
    'DNSRecording': 'Does the domain have valid DNS records?',
    'WebsiteTraffic': 'Does the site have high traffic?',
    'PageRank': 'Does the site have high PageRank?',
    'GoogleIndex': 'Is the website indexed by Google?',
    'LinksPointingToPage': 'Are there many links pointing to this page?',
    'StatsReport': 'Is the site listed in threat reports?'
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
    'DomainRegLen': 'images/DomainRegLen.png',
    'Favicon': 'images/Favicon2.png',
    'NonStdPort': 'images/Non-Standard-Ports.png',
    'HTTPSDomainURL': 'images/httpsdomainurl.png',
    'RequestURL': 'images/requesturl.png',
    'AnchorURL': 'images/AnchorURL.png',
    'LinksInScriptTags': 'images/LinksInScriptTags.png',
    'ServerFormHandler': 'images/formhandler.jpg',
    'InfoEmail': 'images/infoemail.jpg',
    'AbnormalURL': 'images/abnormalURL.png',
    'WebsiteForwarding': 'images/websiteforwarding.png',
    'StatusBarCust': 'images/StatusBarCust.jpg',
    'DisableRightClick': 'images/DisableRightClick.png',
    'UsingPopupWindow': 'images/popup.png',
    'IframeRedirection': 'images/iframe.jpg',
    'AgeofDomain': 'images/DomainAge.jpg',
    'DNSRecording': 'images/DNSRecords.png',
    'WebsiteTraffic': 'images/WebTraffic.jpg',
    'PageRank': 'images/PageRank.jpg',
    'GoogleIndex': 'images/GoogleIndex.png',
    'LinksPointingToPage': 'images/LinksToPage.png',
    'StatsReport': 'images/Statistics-Reports.png'

    
    # ... add the rest here
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
    'DomainRegLen': 'Fig. 9 – Recently registered domain, often used in phishing.',
    'Favicon': 'Fig. 10 – Favicon does not match the legitimate site’s branding.',
    'NonStdPort': 'Fig. 11 – Site uses uncommon network ports, possibly to bypass security.',
    'HTTPSDomainURL': 'Fig. 12 – Misleading domain with “https” in the name but not actually secure.',
    'RequestURL': 'Fig. 13 – Page loads resources from suspicious external domains.',
    'AnchorURL': 'Fig. 14 – Many anchor tags pointing to unrelated or malicious websites.',
    'LinksInScriptTags': 'Fig. 15 – Links hidden inside <script> code to load malicious content.',
    'ServerFormHandler': 'Fig. 16 – Form submission handler points to an untrusted server.',
    'InfoEmail': 'Fig. 17 – Uses free email service (e.g., Gmail, Yahoo) for contact forms.',
    'AbnormalURL': 'Fig. 18 – URL structure is abnormal compared to legitimate sites.',
    'WebsiteForwarding': 'Fig. 19 – Site forwards visitors to another suspicious domain.',
    'StatusBarCust': 'Fig. 20 – Manipulated status bar to display a fake URL.',
    'DisableRightClick': 'Fig. 21 – Right click is disabled on the website',
    'UsingPopupWindow': 'Fig. 22 – Website uses pop-up windows',
    'IframeRedirection': 'Fig. 23 – Page loads inside an iframe (possible redirection)',
    'AgeofDomain': 'Fig. 24 – Domain is very new or has low age',
    'DNSRecording': 'Fig. 25 – Missing or suspicious DNS records',
    'WebsiteTraffic': 'Fig. 26 – Low or suspicious website traffic',
    'PageRank': 'Fig. 27 – Low search engine page rank',
    'GoogleIndex': 'Fig. 28 – Website is not indexed by Google',
    'LinksPointingToPage': 'Fig. 29 – Few or no inbound links to the site',
    'StatsReport': 'Fig. 30 – Suspicious or flagged in statistics/report databases'
}
value_labels = {-1: "🔴 No", 0: "🟡 Not Sure", 1: "🟢 Yes"}
value_options = [-1, 0, 1]

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if not st.session_state.submitted:





    # --- Session state ---
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {}

    # --- UI ---
    st.title("🔐 Phishing Website Detection - Questionnaire")
    st.markdown("Answer the questions one by one to evaluate a website.")

    # --- Progress bar ---
    progress = (st.session_state.current_index + 1) / len(features)
    st.progress(progress, text=f"{int(progress * 100)}% completed")

    # --- Current question ---
    idx = st.session_state.current_index
    feature = features[idx]
    question = feature_question_map[feature]


    st.subheader(f"Question {idx + 1} of {len(features)}")

    # Show image if available
    if feature in feature_image_map:
        st.image(feature_image_map[feature], caption=feature_captions_map[feature])



    # Determine saved or default value
    default_val = st.session_state.answers.get(feature, 0)
    default_idx = value_options.index(default_val) if default_val in value_options else 1



    st.markdown(
        f"<p style='font-size:19px; color:var(--text-color); font-weight:500; margin-bottom:0px; margin-top:0px;'>{question}</p>",
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
    st.session_state.answers[feature] = answer

    # --- Navigation Buttons ---
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        if idx > 0 and st.button("⬅️ Back"):
            st.session_state.current_index -= 1
            st.rerun()


    with col2:
        if idx < len(features) - 1 and st.button("➡️ Next"):
            st.session_state.current_index += 1
            st.rerun()

    # --- Inside col3: Just the button ---
    with col3:
        submit_clicked = False
        if idx == len(features) - 1:

            submit_clicked = st.button("🔍 Submit & Predict")
            st.session_state.submitted = True


# --- Outside the columns: Handle prediction and display results in full width ---
else:
    input_values = [st.session_state.answers.get(f, 0) for f in features]
    prediction = model.predict([input_values])[0]
    proba = model.predict_proba([input_values])[0]

    st.markdown("---")
    st.subheader("🎯 Prediction Result")

    # 🔻 FULL WIDTH STYLED PREDICTION BOX
    with st.container():
        if prediction == 1:
            st.markdown(
                f"""
                <div style='background-color:#d4edda; color:#155724; padding:1rem; border-radius:10px; font-size:18px; width:100%; text-align:center;'>
                    ✅ Website is <strong>LEGITIMATE</strong> with confidence <strong>{proba[1]*100:.2f}%</strong>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.image("images/no-phishing.png")
        else:
            st.markdown(
                f"""
                <div style='background-color:#f8d7da; color:#721c24; padding:1rem; border-radius:10px; font-size:18px; width:100%; text-align:center; margin-bottom:10px;'>
                    🚨 Website is <strong>PHISHING</strong> with confidence <strong>{proba[0]*100:.2f}%</strong>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.image("images/spear-phishing.jpeg")

    # --- Feature Importance ---


         # --- Show User Inputs ---
    st.markdown("---")
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





# In[ ]:




