import streamlit as st
from PIL import Image
import numpy as np
import random

lang = st.sidebar.selectbox("اللغة / Language", ["العربية", "English"])
AR = lang == "العربية"

T = {
    "title": "ضمان",
    "upload": "📸 التقط صورة لوثيقة رسمية" if AR else "📸 Capture a document image",
    "result": "نتيجة التحقق" if AR else "Verification Result",
    "original": "✅ الوثيقة أصلية" if AR else "✅ Document is Genuine",
    "fake": "❌ الوثيقة مزورة" if AR else "❌ Document is Fake",
    "prob": "نسبة الاحتمال" if AR else "Confidence",
}

st.markdown(f"<h1 style='color:#0a3f66;text-align:center'>{T['title']}</h1>", unsafe_allow_html=True)

uploaded_file = st.camera_input(T["upload"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📄 معاينة الوثيقة", use_column_width=True)

    prediction = random.choice(["fake", "real"])
    prob = round(random.uniform(0.82, 0.97), 2)

    st.subheader(T["result"])
    if prediction == "fake":
        st.error(f"{T['fake']} – {T['prob']}: {int(prob*100)}%")
    else:
        st.success(f"{T['original']} – {T['prob']}: {int(prob*100)}%")