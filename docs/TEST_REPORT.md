# รายงานผลการทดสอบระบบ (Test Report)

## 1. ข้อมูลสรุปการทดสอบ
- **ชื่อระบบ:** Web Application สำหรับแสดงผลข้อมูลการจัดการขยะ (Waste Management Dashboard)
- **เครื่องมือทดสอบ:** `pytest`, Streamlit Test Server, Headless Browser Subagent Visual Verification
- **ผลการทดสอบรวม:** ผ่านทั้งหมด (5 Passed, 0 Failed, 0 Error)

---

## 2. รายละเอียดผลการทดสอบ Unit & Integration Tests

| รหัสทดสอบ | ชื่อการทดสอบ | วัตถุประสงค์ | ผลลัพธ์ | หมายเหตุ |
| :--- | :--- | :--- | :--- | :--- |
| `TC-01` | `test_data_loader_reads_raw_data` | ทดสอบการโหลดไฟล์ CSV ภาษาไทย (CP874) และตรวจสอบคอลัมน์สำคัญ | **PASSED** | รองรับทั้งปี 2568 และ 2569 ครบ 579 แถว |
| `TC-02` | `test_data_cleaning_preserves_rows_and_types` | ทดสอบการแปลง Type ตัวเลข การตัดช่องว่าง และการเรียงลำดับ | **PASSED** | แปลงคอลัมน์ตัวเลข 7 คอลัมน์เป็น numeric ถูกต้อง 100% |
| `TC-03` | `test_calculations_match_prototype_2569` | ตรวจสอบผลรวมและการคำนวณตัวชี้วัด (KPIs) เทียบกับเว็บต้นแบบ | **PASSED** | ตัวเลขตรงกับต้นแบบทุกทศนิยม: ขยะเกิด 43,950.65 กก., นำไปใช้ประโยชน์ 9,090.31 กก., ส่งกำจัด 27,691.10 กก. |
| `TC-04` | `test_charts_generate_successfully` | ทดสอบการสร้างออบเจกต์กราฟ Plotly ทั้ง 5 รูปแบบ | **PASSED** | Line Chart, Grouped Bar, Donut, Horizontal Bar, Monthly Staff Bar สมบูรณ์ |
| `TC-05` | `test_empty_dataframe_handling` | ทดสอบกรณีที่ Filter ไม่พบข้อมูล (Dataframe ว่าง) | **PASSED** | ไม่เกิด Error และแสดงกล่องข้อความแจ้งเตือนอย่างเหมาะสม |

---

## 3. ผลการทดสอบด้าน UI และ Visual Verification
ผ่านการเปิดทดสอบจริงผ่าน Browser ที่พอร์ต 8501:
1. **Sidebar Filter:**
   - ฟิลเตอร์ `ปี`: ค่าเริ่มต้น 2569 สามารถเลือก 2568 ได้
   - ฟิลเตอร์ `สังกัด`: ส่วนกลาง, ส่วนภูมิภาค
   - ฟิลเตอร์ `หน่วยงาน`: ปรับเปลี่ยนตามสังกัดอัตโนมัติ
   - ฟิลเตอร์ `เดือน`: เรียงตามลำดับปฏิทินไทย
2. **KPI Metrics:**
   - แสดงผลทั้ง 5 การ์ด ตัวเลขขนาดใหญ่ มีหน่วยวัดชัดเจน
3. **Charts & Visualizations:**
   - Line Chart: แสดงเส้นแนวโน้ม 3 เส้นชัดเจน พร้อม Legend
   - Grouped Bar Chart: แสดงเปรียบเทียบแต่ละหน่วยงาน ชื่อหน่วยงานเอียง 45 องศาอ่านง่าย
   - Donut Chart: แสดงสัดส่วน 75.3% กำจัด vs 24.7% รีไซเคิล
   - Top 10 Horizontal Bar: แสดง 10 อันดับหน่วยงานที่มีขยะเกิดขึ้นสูงสุด
   - Staff Monthly Bar: แสดงจำนวนคนเฉลี่ยตามเดือน
4. **Data Table:**
   - แสดงตารางข้อมูลครบ 11 คอลัมน์ ซ่อน Index Column เพื่อความสะอาดตา

---

## 4. สรุปสถานะความพร้อม
ระบบมีความสมบูรณ์ ตรงตามข้อกำหนดในแผนงาน และพร้อมสำหรับการนำขึ้น GitHub และ Streamlit Community Cloud
