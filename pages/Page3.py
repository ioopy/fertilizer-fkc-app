import streamlit as st
from menu import menu_with_redirect
from utils.func import break_page, get_color_map, get_head_title, hide_header_icons, section_title
import plotly.express as px
from utils.load_data import get_data
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Default page header.
get_head_title(3, "เพื่อโอกาสในการวางกลยุทธ์ทางการตลาด")
# Get data & Filter data
data_all = get_data()
data_all = data_all[['marketplace', 'product_name', 'star_review', 'original_price', 'discount_price_format', 'per_discount_format', 'amount_sold_format', 'total_value', 'itemId', 'shopId']]
data_all = data_all[data_all['per_discount_format'] > 0]
data_all = data_all[data_all['amount_sold_format'] > 0]
data_all = data_all.drop_duplicates()

def get_line_plot(data):
    fig = px.line(data, x='per_discount_format',
                y='total_value', color='product_nm',
                markers=True    
            )
    
    fig.update_layout(
        title={
            'text': '',
            'x': 0.5,  # Center the title
            'xanchor': 'center',  # Ensure it's anchored in the center
            'yanchor': 'top'  # Keep it at the top
        },
        yaxis_title="ยอดขาย",
        xaxis_title="% ส่วนลด",
        xaxis_tickfont_size=16,
        yaxis_tickfont_size=16,
        font=dict(
            size=18,
        ),
        legend=dict(
            orientation="h",        # Set the legend orientation to horizontal
            yanchor="bottom",       # Anchor the legend at the bottom
            y=1,                    # Position the legend above the graph
            xanchor="center",       # Center the legend horizontally
            x=0.5                   # Set the legend to the center of the x-axis
        ),
        margin=dict(
            t=100  # Add space at the top (increase this value as needed)
        ),
        legend_title_text=''
    )
    st.plotly_chart(fig, theme="streamlit")
    return None

def get_scatter_plot(data):
    # mean_discount_price = data['discount_price_format'].mean()
    fig = px.scatter(data, x='per_discount_format', y='total_value', marginal_y="violin",
                color='marketplace',
                size='amount_sold_format', size_max=60,
                hover_name="marketplace", color_discrete_map=get_color_map(),
                labels={'amount_sold_format': 'ยอดขาย (ชิ้น)', 'per_discount_format': '% ส่วนลด', 'total_value': 'ยอดขาย (฿)'},
            )
    fig.update_layout(
        title={
            'text': '',
            'x': 0.5,  # Center the title
            'xanchor': 'center',  # Ensure it's anchored in the center
            'yanchor': 'top'  # Keep it at the top
        },
        yaxis_title="ยอดขาย (฿)",
        xaxis_title="% ส่วนลด",
        xaxis_tickfont_size=16,
        yaxis_tickfont_size=16,
        font=dict(
            size=18,
        ),
        legend=dict(
            orientation="h",        # Set the legend orientation to horizontal
            yanchor="bottom",       # Anchor the legend at the bottom
            y=1,                    # Position the legend above the graph
            xanchor="center",       # Center the legend horizontally
            x=0.5                   # Set the legend to the center of the x-axis
        ),
        margin=dict(
            t=100  # Add space at the top (increase this value as needed)
        ),
        legend_title_text='',
        height=600
    )
    st.plotly_chart(fig, theme="streamlit")
    return None

desc_msg1 = '''
    จากการวิเคราะห์พบว่า:\n
    - ความสัมพันธ์ระหว่างเปอร์เซ็นต์การลดราคาและยอดขายรวม มีค่าสหสัมพันธ์ประมาณ -0.033 ซึ่งบ่งชี้ว่าความสัมพันธ์มีน้อยมากและแทบจะไม่มีผลต่อกัน
    - ความสัมพันธ์ระหว่างเปอร์เซ็นต์การลดราคาและจำนวนสินค้าที่ขายได้ มีค่าสหสัมพันธ์ประมาณ -0.005 ซึ่งแสดงให้เห็นว่าทั้งสองตัวแปรนี้แทบไม่มีความสัมพันธ์กันเลย

'''
summary1 = '''
    ดังนั้นเปอร์เซ็นต์การลดราคาไม่ได้ส่งผลชัดเจนต่อยอดขายหรือจำนวนสินค้าที่ขายได้
'''

desc_msg2 = '''
    จากการวิเคราะห์พบว่า:\n
    - สินค้าที่ลดราคามากกว่า 30% มียอดขายเฉลี่ยอยู่ที่ **34,888.64 บาท**
    - สินค้าที่ลดราคา 30% หรือน้อยกว่านั้นมียอดขายเฉลี่ยสูงกว่าคือ **44,638.58 บาท**
'''
summary2 = '''
    ดังนั้น การลดราคามากกว่า 30% ไม่ได้มีผลทำให้ยอดขายเพิ่มขึ้น ในทางกลับกัน สินค้าที่ลดราคาน้อยกว่ามีแนวโน้มมียอดขายเฉลี่ยสูงกว่า
'''

# Section 1
section_title("เปอร์เซ็นต์การลดราคามีความสัมพันธ์กับยอดขายของสินค้านี้อย่างไร")
data_sorted = data_all.sort_values(by=['per_discount_format', 'amount_sold_format'], ascending=[False, True])
display = data_all.sort_values('per_discount_format', ascending=False)
display = display[['marketplace', 'per_discount_format', 'amount_sold_format', 'total_value']]
display2 = display.groupby('marketplace').agg(
    total_value_sum=('total_value', 'sum'),
    total_value_mean=('total_value', 'mean')
).reset_index()
display2['total_value_mean'] = display2['total_value_mean'].apply(lambda x: f"{x:,.2f}")
display2.rename(columns={'total_value_sum': 'ยอดขายรวม', 'total_value_mean': 'ยอดขายเฉลี่ย'}, inplace=True)
st.dataframe(display2, hide_index=True)
get_scatter_plot(display)
break_page()
st.markdown(desc_msg1)
st.markdown(summary1)

st.divider()
break_page()

# Section 2
section_title("การลดราคามากกว่า 30% มีผลทำให้ยอดขายเพิ่มขึ้นหรือไม่")
data_all = data_all[data_all['per_discount_format'] > 30]
data_sorted = data_all.sort_values(by=['per_discount_format', 'amount_sold_format'], ascending=[False, True])
display = display[display['per_discount_format'] > 30]
display2 = display.groupby('marketplace').agg(
    total_value_sum=('total_value', 'sum'),
    total_value_mean=('total_value', 'mean')
).reset_index()
display2['total_value_mean'] = display2['total_value_mean'].apply(lambda x: f"{x:,.2f}")
display2.rename(columns={'total_value_sum': 'ยอดขายรวม', 'total_value_mean': 'ยอดขายเฉลี่ย'}, inplace=True)
st.dataframe(display2, hide_index=True)
display = display[display['per_discount_format'] > 30]
get_scatter_plot(display)
st.markdown(desc_msg2)
st.markdown(summary2)


