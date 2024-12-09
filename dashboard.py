import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Claim Reimbursement", page_icon = ":bar_chart:", layout = "wide")
st.title("Claim Reimbursement")

path = 'C:/Users/Admin/Downloads/auto_report'

fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df1 = pd.read_excel(path + '/' + filename)

# else:
#     os.chdir(r"C:\Users\AEPAC\Desktop\Streamlit")
#     df = pd.read_csv("Superstore.csv", encoding = "ISO-8859-1")
    
    
# df1 = pd.read_excel(r'C:\Users\Admin\Downloads\auto_report\Fullerton.xlsx')

q1 = df1.groupby(df1['Medical providers'])['Claim paid amount'].sum()
q1 = q1.sort_values(ascending=False).head(10)
q1 = pd.DataFrame({'Hospital':q1.index, 'Money Paid (VND)':q1.values})

q3 = df1['Type of claim submit'].value_counts()
q3 = pd.DataFrame({'Type of claim submit':q3.index, 'Number':q3.values})

q2 = df1.groupby(df1['Chan doan benh'])['Claim paid amount'].sum()
q2 = q2.sort_values(ascending=False).head(10)
q2 = pd.DataFrame({'Treatment Diagnose':q2.index, 'Money Paidv(VND)':q2.values})

df1['Ratio'] = df1['Rejected amount - paid case'] / df1['Request amount']  # Tạo cột tính tỷ lệ
q4 = df1.groupby('Relation')['Ratio'].mean()  # Nhóm theo 'Relation' và tính tổng
q4 = pd.DataFrame({'Relation':q4.index, 'Reject Ratio':q4.values})

chart1, chart2 = st.columns((2))
with chart1:
    st.subheader('Beneficiary type')
    fig = px.pie(values=q3['Number'], names=q3['Type of claim submit'])
    st.plotly_chart(fig,use_container_width=True)
    # fig.update_traces(text = filtered_df["Segment"], textposition = "inside")
    fig.show()
with chart2:
    st.subheader('Top 10 Disease and Amount Money Paid')
    fig = go.Figure(data=[go.Table(
    header=dict(values=list(q2.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=q2.transpose().values.tolist(),
               fill_color='lavender',
               align='left'))])
    
    fig.update_layout(width=600)
    st.plotly_chart(fig,use_container_width=True)
    fig.show()


chart3, chart4 = st.columns((2))
with chart3:
    st.subheader('Reject ratio based on Relation')
    fig = px.bar(q4, x = "Relation", y = "Reject Ratio")
    st.plotly_chart(fig,use_container_width=True)
    fig.show()

with chart4:
    st.subheader('Top 10 Hospital and Amount Money Paid')
    fig = go.Figure(data=[go.Table(
    header=dict(values=list(q1.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=q1.transpose().values.tolist(),
               fill_color='lavender',
               align='left'))])
    
    fig.update_layout(width=600)
    st.plotly_chart(fig,use_container_width=True)
    fig.show()