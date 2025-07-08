import streamlit as st
from PIL import Image
import pytesseract
import difflib
from datetime import datetime
import base64

# قاعدة بيانات داخلية للمستندات الأصلية
DATABASE = {
    "123456": {
        "type": "شهادة جامعية",
        "text": "جامعة السودان للعلوم والتكنولوجيا\nالاسم: طارق أبوبكر\nالرقم الجامعي: 123456\nدرجة البكالوريوس"
    },
    "789101": {
        "type": "بطاقة هوية",
        "text": "جمهورية السودان\nالرقم الوطني: 789101\nالاسم: طارق أبوبكر\nتاريخ الميلاد: 1999"
    },
    "998877": {
        "type": "شهادة خبرة",
        "text": "وزارة التعليم العالي\nالاسم: محمد أحمد\nرقم الملف: 998877\nالمسمى الوظيفي: محاضر"
    }
}

# إعداد صفحة التطبيق
st.set_page_config(page_title="ضمان", layout="centered", page_icon="🛡️")
st.markdown("""
    <style>
    body { background-color: #0f1c2e; }
    .main { background-color: #0f1c2e; color: white; font-family: 'Cairo', sans-serif; }
    .stButton > button {
        background-color: #194569;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 100%;
    }
    .stFileUploader { background-color: #112233; padding: 20px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# العنوان
st.markdown("""
    <h1 style='text-align: right; color: white;'>🛡️ ضمان</h1>
    <p style='text-align: right; color: #cccccc;'>تحقّق من صحة المستندات الرسمية في ثوانٍ</p>
""", unsafe_allow_html=True)

# رفع مستند
uploaded_file = st.file_uploader("\nاسحب المستند هنا أو اختره من جهازك", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file:
    # عرض الوثيقة
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="📄 معاينة الوثيقة", use_column_width=True)

    with st.spinner("🔍 جاري تحليل المستند..."):
        # استخراج النص من الوثيقة
        extracted_text = pytesseract.image_to_string(image, lang='ara')

        # مقارنة النص مع قاعدة البيانات
        matched_ref = None
        for ref, data in DATABASE.items():
            similarity = difflib.SequenceMatcher(None, extracted_text, data['text']).ratio()
            if similarity > 0.7:
                matched_ref = ref
                break

        st.markdown("""<hr style='margin-top:30px;margin-bottom:30px;'>""", unsafe_allow_html=True)

        if matched_ref:
            st.success("✅ المستند سليم")
            st.markdown(f"**الملف:** {uploaded_file.name}")
            st.markdown(f"**رقم المرجع:** {matched_ref}")
            st.markdown(f"**نوع المستند:** {DATABASE[matched_ref]['type']}")

            if st.button("📄 تحميل تقرير التحقق"):
                now = datetime.now().strftime("%Y-%m-%d %H:%M")
                report = f"""
                تقرير التحقق - ضمان\n
                الملف: {uploaded_file.name}
                رقم المرجع: {matched_ref}
                نوع المستند: {DATABASE[matched_ref]['type']}
                النتيجة: ✅ سليم
                التاريخ: {now}
                """
                b64 = base64.b64encode(report.encode()).decode()
                href = f'<a href="data:file/txt;base64,{b64}" download="zaman_report.txt">اضغط هنا لتنزيل التقرير</a>'
                st.markdown(href, unsafe_allow_html=True)
        else:
            st.error("❌ المستند غير مطابق للسجلات الأصلية")
            st.markdown("يرجى التحقق من صحة الوثيقة أو مراجعة الجهة المختصة.")