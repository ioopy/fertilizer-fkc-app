import streamlit as st
from menu import menu_with_redirect
from utils.func import hide_header_icons

st.set_page_config(page_title=f"บทสรุป", page_icon="📍")
st.header(f":blue[บทสรุป]", divider=True)
# st.subheader(sub)

menu_with_redirect()
hide_header_icons()

st.markdown("**สรุปข้อมูลสำคัญจากการวิเคราะห์:**")
desc_msg1 = '''
    1. **Shopee มียอดขายเฉลี่ยสูงกว่า Lazada** ทั้งในกรณีของยอดขายรวมและยอดขายต่อชิ้น แม้ว่า Lazada จะมีอัตราการลดราคาสูงกว่าก็ตาม
    2. **สินค้าที่มีราคาสูงกว่าค่าเฉลี่ย** มีแนวโน้มได้รับคะแนนรีวิวต่ำกว่า ขณะที่สินค้าที่มีราคาต่ำกว่าค่าเฉลี่ยได้รับรีวิวดีกว่า
    3. **เปอร์เซ็นต์การลดราคา** ไม่มีความสัมพันธ์ชัดเจนกับยอดขายหรือจำนวนสินค้าที่ขายได้ การลดราคามากกว่า 30% ไม่ได้เพิ่มยอดขายมากกว่าการลดราคาต่ำกว่า 30%
    4. **สินค้าที่มีราคาหลังหักส่วนลดต่ำกว่าค่าเฉลี่ย** มักจะได้รับคะแนนรีวิวสูงกว่า สินค้าที่มีราคาหลังหักส่วนลดสูงกว่าค่าเฉลี่ย
    5. **พื้นที่ที่ลูกค้าใช้จ่ายมากที่สุด** ได้แก่ กรุงเทพมหานคร สมุทรปราการ และชัยนาท ซึ่งเป็นพื้นที่ที่มียอดขายรวมสูงที่สุดสำหรับสินค้าที่มีราคาสูงหลังหักส่วนลด
'''
st.markdown(desc_msg1)