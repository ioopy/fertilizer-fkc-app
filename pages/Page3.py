import streamlit as st
from menu import menu_with_redirect
from utils.func import break_page, get_head_title, hide_header_icons, section_title
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


# Section 1
section_title("เปอร์เซ็นต์การลดราคามีความสัมพันธ์กับยอดขายของสินค้านี้อย่างไร")
data_sorted = data_all.sort_values(by=['per_discount_format', 'amount_sold_format'], ascending=[False, True])
display = data_all.sort_values('per_discount_format', ascending=False)
st.dataframe(display, hide_index=True)
st.divider()
break_page()

# Section 2
section_title("การลดราคามากกว่า 30% มีผลทำให้ยอดขายเพิ่มขึ้นหรือไม่")
data_all = data_all[data_all['per_discount_format'] > 30]
data_sorted = data_all.sort_values(by=['per_discount_format', 'amount_sold_format'], ascending=[False, True])
display = display[display['per_discount_format'] > 30]
st.dataframe(display, hide_index=True)


