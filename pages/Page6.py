import streamlit as st
from menu import menu_with_redirect
from utils.func import hide_header_icons

st.set_page_config(page_title=f"ข้อเสนอแนะเพิ่มเติม", page_icon="📈")
st.header(f":blue[ข้อเสนอแนะเพิ่มเติม]", divider=True)
# st.subheader(sub)

menu_with_redirect()
hide_header_icons()


desc_msg1 = '''
    **1. การตั้งราคาสินค้า:** จากผลการวิเคราะห์พบว่าสินค้าที่มีราคาต่ำกว่าค่าเฉลี่ยมักได้รับรีวิวที่ดีกว่า ซึ่งแสดงว่าผู้บริโภคมีแนวโน้มพึงพอใจมากขึ้นเมื่อได้รับสินค้าคุณภาพที่ราคาถูกกว่า ดังนั้น การตั้งราคาที่เหมาะสมอาจช่วยกระตุ้นให้เกิดการรีวิวที่ดีขึ้นและกระตุ้นยอดขายได้
    
    **2. การใช้ส่วนลดในการกระตุ้นยอดขาย:** แม้ว่าจะพบว่าการลดราคามากกว่า 30% ไม่ได้ส่งผลชัดเจนในการเพิ่มยอดขาย อาจเป็นไปได้ว่าการลดราคามากเกินไปทำให้ผู้ซื้อรับรู้ว่าสินค้าอาจมีคุณภาพไม่ดี ดังนั้นการใช้ส่วนลดในระดับที่เหมาะสม และผสมผสานกับการโปรโมตคุณภาพของสินค้าอาจได้ผลดีกว่า

    **3. การเพิ่มรีวิวที่ดี:** ผลลัพธ์บ่งชี้ว่าการตั้งราคาต่ำกว่าค่าเฉลี่ยช่วยให้ได้รับรีวิวที่ดีกว่า ดังนั้น การตั้งราคาที่สอดคล้องกับคุณภาพของสินค้า รวมถึงการกระตุ้นให้ลูกค้ารีวิวสินค้า เช่น ผ่านการให้สิทธิพิเศษหรือโปรโมชันเพิ่มเติมสำหรับผู้ที่เขียนรีวิว อาจช่วยสร้างภาพลักษณ์ที่ดีขึ้น

    **4. แพลตฟอร์มที่ควรมุ่งเน้น:** Shopee มีแนวโน้มที่จะสร้างยอดขายเฉลี่ยที่สูงกว่ามากเมื่อเปรียบเทียบกับ Lazada ดังนั้นธุรกิจที่ต้องการกระตุ้นยอดขายอาจพิจารณาเน้นการทำการตลาดใน Shopee มากกว่า Lazada หรือใช้กลยุทธ์ที่แตกต่างกันในแต่ละแพลตฟอร์ม
    
    การประเมินผลข้อมูลเชิงลึกเหล่านี้สามารถช่วยในการปรับแผนการตลาดและกลยุทธ์การขาย เพื่อเพิ่มประสิทธิภาพการขายในอนาคต
'''
st.markdown(desc_msg1)



