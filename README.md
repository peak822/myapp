# ♻️ Waste Management Dashboard (Streamlit)

เว็บแอปพลิเคชันสำหรับวิเคราะห์และแสดงผลข้อมูลการจัดการขยะมูลฝอยภายในหน่วยงาน พัฒนาด้วย **Python**, **Pandas** และ **Streamlit** พร้อมการแสดงผลข้อมูลเชิงโต้ตอบด้วย **Plotly**

---

## 📌 แหล่งข้อมูล (Data Sources)
- **Dataset:** [ปริมาณขยะมูลฝอย - กรมอุทยานแห่งชาติ สัตว์ป่า และพันธุ์พืช (data.go.th)](https://data.go.th/dataset/gdpublish-69-dnp01-11-01)
- **เว็บต้นแบบอ้างอิง:** [Waste Management Dashboard (Streamlit App)](https://7magv62oy73s4kfhpjlbbg.streamlit.app/)

---

## ✨ ฟีเจอร์หลัก (Features)

1. **ตัวกรองข้อมูลเชิงโต้ตอบ (Interactive Filters):**
   - กรองตาม **ปี (Year)**: พ.ศ. 2568, 2569
   - กรองตาม **สังกัด (Affiliation)**: ส่วนกลาง, ส่วนภูมิภาค
   - กรองตาม **หน่วยงาน (Department)**: อัปเดตรายชื่อหน่วยงานตามสังกัดที่เลือกโดยอัตโนมัติ
   - กรองตาม **เดือน (Month)**: เลือกดูข้อมูลเฉพาะเดือนที่ต้องการได้
2. **สรุปภาพรวมตัวชี้วัด (KPI Cards):**
   - ขยะที่เกิดขึ้นทั้งหมด (กก.)
   - ปริมาณขยะที่นำไปใช้ประโยชน์ (กก.)
   - ปริมาณขยะที่ส่งกำจัด (กก.)
   - ค่าเฉลี่ยร้อยละขยะส่งกำจัดลดลง (%)
   - โฟมบรรจุอาหาร (ใบ)
3. **การแสดงผลกราฟิก (Data Visualizations - 5 กราฟ):**
   - 📈 **Line Chart:** แนวโน้มปริมาณขยะรายเดือน เปรียบเทียบ 3 ประเภท (เกิดขึ้น, นำไปใช้ประโยชน์, ส่งกำจัด)
   - 🏢 **Grouped Bar Chart:** เปรียบเทียบปริมาณขยะตามหน่วยงานต่าง ๆ
   - 🍩 **Donut Chart:** สัดส่วนการจัดการขยะ (ส่งกำจัด vs นำไปใช้ประโยชน์)
   - 📊 **Horizontal Bar Chart:** 10 อันดับหน่วยงานที่มีขยะเกิดขึ้นสูงสุด
   - 👥 **Bar Chart:** จำนวนคนเฉลี่ยรายเดือน
4. **ตารางรายละเอียดข้อมูล (Data Table):**
   - แสดงตารางข้อมูลดิบที่ผ่านการกรองตามเงื่อนไข พร้อมระบบค้นหาและจัดเรียงข้อมูล

---

## 📁 โครงสร้างโปรเจกต์ (Project Structure)

```text
Final/
├── app.py                      # สคริปต์หลักสำหรับรัน Streamlit Web Application
├── requirements.txt            # รายการไลบรารีที่จำเป็น
├── README.md                   # คู่มือแนะนำโปรเจกต์และการติดตั้ง
├── .gitignore                  # กำหนดไฟล์ที่ไม่ต้องการนำขึ้น Git
│
├── data/
│   ├── raw/                    # ข้อมูลดิบจาก data.go.th (waste_2568.csv, waste_2569.csv)
│   └── processed/              # ข้อมูลที่ผ่านการทำความสะอาดและรวมไฟล์ (waste_data_combined.csv)
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # โหลดไฟล์ CSV และจัดการการเข้ารหัส (CP874 / UTF-8)
│   ├── data_cleaning.py        # ทำความสะอาดข้อมูล แปลงชนิดข้อมูล และจัดเรียง
│   └── charts.py               # ฟังก์ชันสำหรับสร้างกราฟ Plotly
│
├── docs/
│   ├── UI_REFERENCE.md         # เอกสารวิเคราะห์เว็บต้นแบบ
│   ├── DATA_DICTIONARY.md      # พจนานุกรมข้อมูลและรายละเอียดคอลัมน์
│   └── TEST_REPORT.md          # รายงานสรุปผลการทดสอบระบบ
│
├── plan/
│   └── streamlit_data_visualization_plan.md   # แผนการดำเนินงานโปรเจกต์
│
└── tests/
    └── test_data.py            # การทดสอบ Unit Test ตรวจสอบความถูกต้องของข้อมูลและกราฟ
```

---

## 🚀 การติดตั้งและรันโปรเจกต์ในเครื่อง (Local Setup)

### 1. ติดตั้ง Dependencies
เปิด Terminal หรือ Command Prompt ในโฟลเดอร์โปรเจกต์ แล้วรันคำสั่ง:

```bash
pip install -r requirements.txt
```

### 2. รันแอปพลิเคชัน Streamlit
รันคำสั่ง:

```bash
streamlit run app.py
```

เมื่อรันสำเร็จ แอปจะเปิดขึ้นมาที่เบราว์เซอร์อัตโนมัติที่ `http://localhost:8501`

---

## 🧪 การรันชุดทดสอบ (Testing)

โปรเจกต์มี Unit Tests ครอบคลุมการโหลดข้อมูล การคลีนข้อมูล และการสร้างกราฟทั้งหมด สามารถรันได้ด้วยคำสั่ง:

```bash
python -m pytest -v
```

---

## ☁️ ขั้นตอนการ Deploy บน Streamlit Community Cloud

1. **สร้าง GitHub Repository:**
   - เริ่มต้น Git Repository:
     ```bash
     git init
     git add .
     git commit -m "Initial commit: Waste Management Dashboard"
     ```
   - นำขึ้น GitHub (Remote):
     ```bash
     git branch -M main
     git remote add origin https://github.com/<your-username>/<your-repo-name>.git
     git push -u origin main
     ```
2. **Deploy บน Streamlit Cloud:**
   - ไปที่ [share.streamlit.io](https://share.streamlit.io/)
   - ล็อกอินด้วยบัญชี GitHub
   - คลิก **"New app"**
   - เลือก Repository และ Branch `main`
   - ตั้งค่า **Main file path** เป็น `app.py`
   - คลิก **"Deploy"**
