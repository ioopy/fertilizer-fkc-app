import streamlit as st
import pandas as pd
import plotly.express as px
from utils.func import break_page, get_head_title, section_title
from utils.load_data import get_data
import plotly.graph_objects as go
import numpy as np

get_head_title(5, "เพื่อหาช่องทางการขายที่เหมาะสม")

def get_bar_plot(data, title, is_grop=False):
    marketplace_colors = {
        'shopee': '#FE6132',
        'lazada': '#0F0C76 ',
    }
    # data = data[data['total_value'] > 0]

    data['text'] = np.where(data['total_value'] == 0, '', data['total_value'].apply(lambda x: f'{x:,.2f}'))
    data['color'] = data['marketplace'].map(marketplace_colors)
    fig = px.bar(
            data,
            x='total_value', 
            y='discount_range',
            color=data["marketplace"],
            color_discrete_map=marketplace_colors,
            orientation='h',
            barmode='group',
            height=600,
            text='text',
            labels={'discount_range': 'ส่วนลด', 'total_value': 'ยอดขาย (฿)', 'star_review': 'คะแนน', },
        )        
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_xaxes(range=[1, 67000000], title_text="ยอดขาย")
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,  # Center the title
            'xanchor': 'center',  # Ensure it's anchored in the center
            'yanchor': 'top'  # Keep it at the top
        },
        xaxis_tickfont_size=16,
        yaxis_tickfont_size=16,
        font=dict(
            size=18,
        ),
        yaxis_title="% ส่วนลด",
        xaxis_title="ยอดขาย",
        legend_title_text='',
        legend=dict(
            orientation="h",        # Set the legend orientation to horizontal
            yanchor="bottom",       # Anchor the legend at the bottom
            y=1,                    # Position the legend above the graph
            xanchor="center",       # Center the legend horizontally
            x=0.5                   # Set the legend to the center of the x-axis
        ),
    )
    st.plotly_chart(fig, theme="streamlit")

def get_bar_comparison(data):
    marketplace_colors = {
        'shopee': '#FE6132',
        'lazada': '#0F0C76',
    }
    
    # Assuming data['marketplace'] contains categorical data for Shopee and Lazada
    data['color'] = data['marketplace'].map(marketplace_colors)

    fig = go.Figure()

    # Adding Shopee's total_value (y-axis 1)
    fig.add_trace(
        go.Bar(
            x=data['marketplace'],  # Categories (Shopee, Lazada)
            y=data['total_value'],  # First Y-axis (total_value)
            name='ยอดขาย',
            marker=dict(color='#386641'),
            text=data['total_value'],
            textposition='auto',
            texttemplate='%{text:,.0f}',
            offsetgroup=1,  
            yaxis='y1'  # Associate with the first y-axis
        )
    )

    # Adding Lazada's amount_sold_format (y-axis 2)
    fig.add_trace(
        go.Bar(
            x=data['marketplace'],
            y=data['amount_sold_format'],  # Second Y-axis (amount_sold_format)
            name='จำนวนขาย (ชิ้น)',
            marker=dict(color='#a7c957'),
            text=data['amount_sold_format'],
            textposition='auto',
            texttemplate='%{text:,.0f}',
            offsetgroup=2,  
            yaxis='y2'  # Associate with the second y-axis
        )
    )

    # Update layout with dual y-axes
    fig.update_layout(
        barmode='group',  # Group bars together by marketplace
        title='',
        xaxis=dict(
            title="",
            tickfont_size=16
        ),
        yaxis=dict(
            title="ยอดขาย",  # Title for the first y-axis
            tickfont_size=16,
            showgrid=False,  # Optionally, hide grid for clarity
        ),
        yaxis2=dict(
            title="จำนวนขาย (ชิ้น)",  # Title for the second y-axis
            overlaying='y',  # Overlay the second y-axis with the first one
            side='right',  # Place the second y-axis on the right side
            tickfont_size=16,
            showgrid=False  # Optionally, hide grid for clarity
        ),
        font=dict(size=18),
        legend=dict(
            orientation="h",        # Set the legend orientation to horizontal
            yanchor="bottom",       # Anchor the legend at the bottom
            y=1,                    # Position the legend above the graph
            xanchor="center",       # Center the legend horizontally
            x=0.5                   # Set the legend to the center of the x-axis
        ),
        legend_title_text='',
        showlegend=True
    )

    st.plotly_chart(fig, theme="streamlit")

    return None

desc_msg1 = '''
    จากการวิเคราะห์พบว่า:\n
    - Lazada มีอัตราการลดราคาสินค้าเฉลี่ยสูงกว่าที่ประมาณ 18.11%
    - Shopee มีอัตราการลดราคาสินค้าเฉลี่ยอยู่ที่ประมาณ 9.07%

'''
summary1 = '''
    อย่างไรก็ตาม แม้ว่า Lazada จะมีอัตราการลดราคาสูงกว่า แต่ยอดขายเฉลี่ยของ Shopee ยังคงสูงกว่ามาก โดยยอดขายเฉลี่ยของ Shopee อยู่ที่ประมาณ 138,565.68 บาท ขณะที่ Lazada มียอดขายเฉลี่ยที่ 38,353.02 บาท\n
    ดังนั้น แม้ Lazada จะมีอัตราการลดราคาสูงกว่า แต่ยอดขายของ Shopee ยังสูงกว่ามาก
'''

desc_msg2 = '''
    จากการวิเคราะห์พบว่า:\n
    - สินค้าที่มีส่วนลดสูงสุดใน **Shopee** อยู่ในช่วง **0-10%**  โดยมียอดขายรวม **56,193,614 บาท**
    - สินค้าที่มีส่วนลดสูงสุดใน **Lazada** อยู่ในช่วง **0-10%** โดยมียอดขายรวม **29,829,784.17 บาท**
'''
summary2 = '''
    สินค้าที่มีส่วนลดสูงสุดใน Shopee มียอดขายสูงกว่า Lazada โดยยอดขายใน Shopee สูงกว่าถึงประมาณ 2 เท่า
'''

data_all = get_data()
data_all = data_all[['marketplace', 'per_discount_format', 'amount_sold_format', 'total_value']]
data_all = data_all[data_all['amount_sold_format'] > 0]

section_title("แพลตฟอร์มใด (Shopee หรือ Lazada) มีอัตราการลดราคาสินค้าโดยเฉลี่ยมากกว่ากัน และมีผลต่อยอดขายอย่างไร")
mean_total_value = data_all['total_value'].mean()
mean_amount_sold = data_all['amount_sold_format'].mean()
discount_stats = data_all.groupby('marketplace').agg({
    'amount_sold_format': 'sum',
    'total_value': 'sum'
}).reset_index()

discount_stats_display = data_all.groupby('marketplace').agg({
    'per_discount_format': 'mean',
    'amount_sold_format': 'sum',
    'total_value': 'sum'
}).reset_index()
discount_stats_display['per_discount_format'] = discount_stats_display['per_discount_format'].apply(lambda x: f"{x:.2f}%")
discount_stats_display.rename(columns={'per_discount_format': 'ค่าเฉลี่ยส่วนลด', 'amount_sold_format': 'ยอดขาย (ชิ้น)', 'total_value': 'ยอดขาย'}, inplace=True)
st.dataframe(discount_stats_display, hide_index=True)
discount_stats = discount_stats.sort_values(by='marketplace', ascending=False)
get_bar_comparison(discount_stats)
st.markdown(desc_msg1)
st.markdown(summary1)
break_page()

# st.divider()
# break_page()
section_title("ยอดขายของสินค้าที่มีส่วนลดสูงสุดใน Shopee และ Lazada แตกต่างกันมากน้อยเพียงใด")
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
labels = ['0-10%', '11-20%', '21-30%', '31-40%', '41-50%', '51-60%', '61-70%', '71-80%', '81-90%', '91-100%']
data_all['discount_range'] = pd.cut(data_all['per_discount_format'], bins=bins, labels=labels, include_lowest=True)
discount_summary = data_all.groupby(['marketplace','discount_range'])['total_value'].sum().reset_index()
# discount_summary = discount_summary.sort_values(by=['total_value'], ascending=[True])
get_bar_plot(discount_summary, "")
st.markdown(desc_msg2)
st.markdown(summary2)
