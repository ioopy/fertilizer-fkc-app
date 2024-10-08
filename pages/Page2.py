import streamlit as st
import plotly.express as px
from utils.func import break_page, get_head_title, section_title
from utils.load_data import get_data

# Default page header.
get_head_title(2, "เพื่อโอกาสในการพัฒนาสินค้า")
# Get data & Filter data
data_all = get_data()
data_all = data_all[['marketplace', 'product_name', 'star_review', 'original_price', 'discount_price_format', 'amount_sold_format', 'itemId', 'shopId']]
data_all = data_all[data_all['amount_sold_format'] > 0]

def get_bar_plot(data, title, mean_star_review):
    data = data.sort_values('star_review', ascending=True)
    data.rename(columns={'star_review': 'คะแนน'}, inplace=True)
    fig = px.bar(
            data,
            x='คะแนน', 
            y='product_nm',
            color=data["marketplace"],
            orientation='h',
            barmode='group',
            text='คะแนน',
            height=600,
        )      
    fig.update_traces(texttemplate='%{text:.2f}', textposition='auto')
    fig.add_shape(
        type="line",
        x0=mean_star_review, x1=mean_star_review,   # Line will be vertical at the mean
        y0=0, y1=1,   # Line spans the full y-axis (relative to the axis range)
        xref="x", yref="paper",   # xref is for x-axis, yref="paper" means span full y-axis
        line=dict(color="red", width=2, dash="dash")  # Red dashed line for mean
    )
    fig.add_annotation(
        x=mean_star_review,
        y=1.05,  # Position above the plot
        xref="x", yref="paper",
        text=f"ค่าเฉลี่ยรีวิว: {mean_star_review:.2f}",
        showarrow=False,
        font=dict(size=14, color="red")
    )

    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,  # Center the title
            'xanchor': 'center',  # Ensure it's anchored in the center
            'yanchor': 'top'  # Keep it at the top
        },
        yaxis_title="",
        xaxis_title="คะแนน",
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
        legend_title_text=''
    )
    st.plotly_chart(fig, theme="streamlit")

def get_scatter_plot(data):
    mean_original_price = data['original_price'].mean()
    fig = px.scatter(data, x='star_review', y='original_price',
                    labels={'star_review': 'คะแนนรีวิว', 'original_price': 'ราคาก่อนลด', 'total_value': 'ยอดขาย (฿)'},
                # symbol='product_nm',
                # trendline='ols'
            )
    fig.add_shape(
        type="line",
        x0=0, x1=1,  # Line will span the full x-axis
        y0=mean_original_price, y1=mean_original_price,  # Horizontal line at mean price
        xref="paper", yref="y",  # xref="paper" for full x-axis span, yref="y" for mean on y-axis
        line=dict(color="red", width=2, dash="dash")  # Red dashed line for the mean price
    )

    # Add an annotation for the mean price line
    fig.add_annotation(
        x=0.1,  # Position right to the plot
        y=mean_original_price + (mean_original_price * 2),
        xref="paper", yref="y",
        text=f"ราคาเฉลี่ย: {mean_original_price:.2f}",
        showarrow=False,
        font=dict(size=14, color="red")
    )
    fig.update_layout(
        title={
            'text': '',
            'x': 0.5,  # Center the title
            'xanchor': 'center',  # Ensure it's anchored in the center
            'yanchor': 'top'  # Keep it at the top
        },
        yaxis_title="ราคาสินค้า",
        xaxis_title="คะแนนรีวิว",
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

desc_msg1 = '''
    **สินค้าที่มียอดรีวิวสูงกว่าค่าเฉลี่ยในแต่ละแพลตฟอร์ม ได้แก่:**
'''
desc_msg2 = '''
    จากการวิเคราะห์พบว่า:\n
    - สินค้าที่มีราคาสูงกว่าค่าเฉลี่ยมีคะแนนรีวิวเฉลี่ยอยู่ที่ **3.68 ดาว**
    - สินค้าที่มีราคาต่ำกว่าค่าเฉลี่ยมีคะแนนรีวิวเฉลี่ยอยู่ที่ **4.27 ดาว**
'''
summary2 = '''
    ดังนั้น สินค้าที่มีราคาสูงกว่าค่าเฉลี่ยมีแนวโน้มได้รับรีวิวต่ำกว่าสินค้าที่มีราคาต่ำกว่าค่าเฉลี่ยอย่างชัดเจน
'''

# Section 1
section_title("สินค้าที่มียอดรีวิวเฉลี่ยสูงที่สุดในแต่ละแพลตฟอร์มคืออะไร")
mean_star_review = data_all['star_review'].mean()
st.markdown(f"**คะแนนรีวิวเฉลี่ย : {mean_star_review:.2f}**")
grouped_df = data_all.groupby(['marketplace', 'product_name', 'itemId', 'shopId'])['star_review'].mean().reset_index()
display = grouped_df[grouped_df['star_review'] > mean_star_review]
display = display[['marketplace', 'product_name', 'star_review']]
display = display.sort_values('star_review', ascending=False)
display.rename(columns={'product_name': 'สินค้า', 'star_review': 'คะแนนรีวิว'}, inplace=True)

st.markdown(desc_msg1)
st.write("**Shopee**")
display_shopee = display[display['marketplace'] == 'shopee']
st.dataframe(display_shopee, hide_index=True)
break_page()
st.write("**Lazada**")
display_lazada = display[display['marketplace'] == 'lazada']
st.dataframe(display_lazada, hide_index=True)
# get_bar_plot(grouped_df, "", mean_star_review)

st.divider()
break_page()
# Section 2
section_title("สินค้าราคาสูงกว่าค่าเฉลี่ยมีแนวโน้มได้รับรีวิวต่ำกว่าสินค้าราคาต่ำกว่าค่าเฉลี่ยหรือไม่")
display = grouped_df.sort_values('star_review', ascending=False)
# st.dataframe(display, hide_index=True)
# st.write(data_all)
get_scatter_plot(data_all)
st.markdown(desc_msg2)
st.markdown(summary2)
