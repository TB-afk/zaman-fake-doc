import streamlit as st
from PIL import Image
import random

st.set_page_config(page_title="ضمان", layout="centered")

# --- الشعار والواجهة ---
st.markdown("""
    <div style='background-color:#0a1f33;padding:1rem 2rem;border-radius:12px;margin-bottom:2rem;display:flex;align-items:center'>
        <img src="https://i.imgur.com/8fKQK9L.png" style='height:40px;margin-left:10px'/>
        <h1 style='color:white;margin:0;font-size:30px'>ضمان</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown(
    "<h3 style='color:#ccc;'>تحقّق كشف المستندات رسميًا بالكاميرا أو رفع الملف</h3>",
    unsafe_allow_html=True
)

# --- رفع أو تصوير مستند ---
st.markdown("<hr>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    camera_file = st.camera_input("📸 التقط مستند بالكاميرا")
with col2:
    upload_file = st.file_uploader("🗂️ أو اختر ملف من جهازك", type=["png", "jpg", "jpeg"])

doc = camera_file or upload_file

# --- المعالجة والنتيجة ---
if doc:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("📊 جاري تحليل المستند...")

    image = Image.open(doc)
    st.image(image, caption="📄 معاينة المستند", use_column_width=True)

    # محاكاة النتيجة
    is_fake = random.choice([True, False])
    prob = round(random.uniform(0.83, 0.97), 2)
    doc_type = random.choice(["شهادة جامعية", "بطاقة هوية", "عقد عمل"])
    ref_number = random.randint(100000, 999999)

    if is_fake:
        st.error(f"❌ المستند مزوّر")
    else:
        st.success("✅ المستند سليم")

    st.markdown(f"""
        <div style='color:#ddd;margin-top:1rem'>
        📄 اسم الملف: document.jpg<br>
        🔖 رقم المرجع: <code>{ref_number}</code><br>
        🗂️ نوع المستند: {doc_type}<br>
        🔍 نسبة التأكد: {int(prob*100)}%
        </div>
    """, unsafe_allow_html=True)

    st.download_button("📥 تحميل تقرير التحقق", data=f"رقم المرجع: {ref_number}\nنوع الوثيقة: {doc_type}\nالنتيجة: {'مزور' if is_fake else 'سليم'}", file_name="report.txt")