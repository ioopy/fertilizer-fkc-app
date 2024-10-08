import streamlit as st
from utils.func import break_page, get_color_map, get_head_title, section_title
from utils.load_data import get_data
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Default page header.
get_head_title(1, "เพื่อศึกษาแบรนด์ที่ยอดขายสูง")
# Get data & Filter data
data_all = get_data()
data_all = data_all[['marketplace', 'product_name', 'amount_sold_format', 'discount_price_format', 'total_value', 'per_discount_format', 'itemId', 'shopId', 'star_review']]
data_all = data_all[data_all['amount_sold_format'] > 0]

def get_bar_plot(data, title):
    data = data.sort_values('total_value', ascending=False)
    data.rename(columns={'total_value': 'ยอดขาย'}, inplace=True)
    fig = px.bar(
        data,
        x='ยอดขาย', 
        y='marketplace',
        color=data["marketplace"],
        orientation='h',
        text='ยอดขาย',
        color_discrete_map=get_color_map(),
    ) 
    
    fig.update_traces(texttemplate='%{text:.2s}', textposition='auto')
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,  # Center the title
            'xanchor': 'center',  # Ensure it's anchored in the center
            'yanchor': 'top'  # Keep it at the top
        },
        yaxis_title="",
        xaxis_title="ยอดขาย",
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

def get_bar_plot_group(data, title):

    sorted_df_final = data.sort_values(by=['marketplace', 'amount_sold_format'], ascending=[False, True])
    sorted_df_final.rename(columns={'amount_sold_format': 'ยอดขาย'}, inplace=True)
    fig = px.bar(
        sorted_df_final,
        x='ยอดขาย', 
        y='product_nm',
        color=sorted_df_final["marketplace"],
        orientation='h',
        barmode='group',
        height=700,
        color_discrete_map=get_color_map(),
        text='ยอดขาย')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='auto')
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,  # Center the title
            'xanchor': 'center',  # Ensure it's anchored in the center
            'yanchor': 'top'  # Keep it at the top
        },
        yaxis_title="",
        xaxis_title="ยอดขาย (ชิ้น)",
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

def get_line_comparision(data, title):
    fig = make_subplots(rows=2, cols=2, 
                        shared_yaxes=False,  # Share the y-axis (province)
                        subplot_titles=["จำนวนขาย (ชิ้น)", "ราคาขาย", "% ส่วนลด", "คะแนน"],  # Titles for the subplots
                        horizontal_spacing=0.12, 
                        ) 

    fig.add_trace(go.Scatter(
        x=data['total_value'],
        y=data['amount_sold_format'],
        line=dict(color='#1f77b4',width=2),
        line_shape='linear'
    ),
    row=1, col=1 )


    fig.add_trace(go.Scatter(
        x=data['total_value'],
        y=data['discount_price_format'],
        line=dict(color='#ff7f0e',width=2),
        line_shape='linear'
    ),
    row=1, col=2 )

    fig.add_trace(go.Scatter(
        x=data['total_value'],
        y=data['per_discount_format'],
        line=dict(color='#d62728',width=2, dash='dot'),
        line_shape='linear'
    ),
    row=2, col=1 )

    fig.add_trace(go.Scatter(
        x=data['total_value'],
        y=data['star_review'],
        line=dict(color='#9467bd',width=2, dash='dot'),
        line_shape='linear'
    ),
    row=2, col=2 )

    fig.update_xaxes(title_text="ยอดขาย", row=1, col=1)
    fig.update_xaxes(title_text="ยอดขาย", row=1, col=2)
    fig.update_xaxes(title_text="ยอดขาย", row=2, col=1)
    fig.update_xaxes(title_text="ยอดขาย", row=2, col=2)

    fig.update_yaxes(title_text="จำนวนขาย (ชิ้น)", row=1, col=1)
    fig.update_yaxes(title_text="ราคาขาย", row=1, col=2)
    fig.update_yaxes(title_text="% ส่วนลด", row=2, col=1)
    fig.update_yaxes(title_text="คะแนน", row=2, col=2)
    # Update layout properties
    fig.update_layout(
        title_text=title,
        width=800,
        height=700,
        showlegend=False,
    )

    st.plotly_chart(fig, theme="streamlit")

desc_msg1 = '''
    จากการวิเคราะห์ข้อมูล พบว่า:\n
    - Shopee มียอดขายเฉลี่ยของสินค้าสูงกว่า Lazada อย่างชัดเจน โดยยอดขายเฉลี่ยของ Shopee อยู่ที่ประมาณ **138,565.68 บาท**
    - ในขณะที่ยอดขายเฉลี่ยของ Lazada อยู่ที่ประมาณ **38,353.02 บาท**
'''
summary1 = '''
    สรุปได้ว่า Shopee มียอดขายเฉลี่ยของสินค้าสูงกว่ามากเมื่อเปรียบเทียบกับ Lazada
'''

desc_msg2 = '''
    จากการวิเคราะห์ยอดขายเฉลี่ยของสินค้าระหว่าง Shopee และ Lazada โดยพิจารณาปัจจัยเพิ่มเติม พบว่า:\n
    **Shopee**:\n 
    - จำนวนสินค้าที่ขายเฉลี่ย: 1,417 ชิ้น
    - ราคาหลังหักส่วนลดเฉลี่ย: 134.92 บาท
    - เปอร์เซ็นต์การลดราคาเฉลี่ย: 8.94%
    - คะแนนรีวิวเฉลี่ย: 4.27 ดาว

    **Lazada**:\n
    - จำนวนสินค้าที่ขายเฉลี่ย: 107 ชิ้น
    - ราคาหลังหักส่วนลดเฉลี่ย: 414.06 บาท
    - เปอร์เซ็นต์การลดราคาเฉลี่ย: 18.12%
    - คะแนนรีวิวเฉลี่ย: 4.12 ดาว
'''
summary2 = '''
    จากข้อมูลนี้ เราพบว่า Shopee มีจำนวนสินค้าที่ขายเฉลี่ยสูงกว่า Lazada อย่างมาก ในขณะที่ราคาหลังหักส่วนลดใน Lazada สูงกว่ามาก
'''

# Section 1
section_title("ระหว่าง Shopee และ Lazada แพลตฟอร์มใดที่มียอดขายเฉลี่ยของสินค้าสูงกว่ากัน")
grouped_df = data_all.groupby('marketplace')['total_value'].sum().reset_index()

display = data_all.groupby('marketplace').agg(
    total_value_sum=('total_value', 'sum'),
    total_value_mean=('total_value', 'mean')
).reset_index()

display['total_value_mean'] = display['total_value_mean'].apply(lambda x: f"{x:,.2f}")
display.rename(columns={'total_value_sum': 'ยอดขายรวม', 'total_value_mean': 'ยอดขายเฉลี่ย'}, inplace=True)
st.dataframe(display, hide_index=True)
get_bar_plot(grouped_df, "")
st.markdown(desc_msg1)
st.markdown(summary1)

st.divider()
break_page()

# Section 2
section_title("สินค้าที่ขายดีที่สุดใน Shopee และ Lazada แตกต่างกันมากน้อยเพียงใด")

shopee = data_all[data_all['marketplace'] == 'shopee']
shopee = shopee.sort_values('total_value', ascending=False)
shopee = shopee.drop_duplicates()
shopee = shopee.head(10)
get_line_comparision(shopee, "Shopee 10 อันดับสินค้าที่ขายดี")
break_page()
lazada = data_all[data_all['marketplace'] == 'lazada']
lazada = lazada.sort_values('total_value', ascending=False)
lazada = lazada.drop_duplicates()
lazada = lazada.head(10)
get_line_comparision(lazada, "Lazada 10 อันดับสินค้าที่ขายดี")

st.markdown(desc_msg2)
st.markdown(summary2)



