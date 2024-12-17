import duckdb
import pandas as pd
import plotly.express as px
# import plotly.graph_objects as go
import streamlit as st
# import subprocess
# import webbrowser
# import psutil 
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from PIL import Image
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# import time
# import os

# Mở ứng dụng Streamlit trong trình duyệt
def open_browser():
    url = "http://localhost:8501"
    webbrowser.open(url)
#######################################
# PAGE SETUP
#######################################

st.set_page_config(page_title="Claim Dashboard", page_icon=":bar_chart:", layout="wide")

# Thêm CSS để căn giữa
st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)


with st.sidebar:
    st.header("UPLOAD YOUR FILE")
    uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True, type=["csv", "xlsx", "xls"])
    if not uploaded_files:
        st.info("Upload files", icon="ℹ️")
        st.stop()

    #######################################
    # DATA LOADING
    #######################################

    @st.cache_data
    def load_data(file):
        if file.name.endswith(".xlsx"):
            return pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file.name}")
            return None
    st.title("Tiêu chí phân tích")
    
    if "active_group" not in st.session_state:
        st.session_state["active_group"] = "group_1"

# Tạo radio button để chọn nhóm
    selected_group = st.radio(
        "Chọn nhóm báo cáo:",
        ["Báo cáo bồi thường", "Báo cáo y khoa/Nhân khẩu học"],
        index=0 if st.session_state["active_group"] == "group_1" else 1
    )

    # Cập nhật trạng thái nhóm được chọn
    if selected_group == "Báo cáo bồi thường":
        st.session_state["active_group"] = "group_1"
    else:
        st.session_state["active_group"] = "group_2"

    # Hiển thị selectbox tương ứng với nhóm đã chọn
    if st.session_state["active_group"] == "group_1":
        st.session_state["selected_option_group1"] = st.selectbox(
            "Báo cáo bồi thường",
            ["Báo cáo tỉ lệ bồi thường", "Báo cáo loại hình bồi thường", "Báo cáo theo quyền lợi","Báo cáo theo chi nhánh/Tập đoàn"],
            index=st.session_state.get("selected_option_group1_index", 0)
        )
        # Lưu lại lựa chọn
st.session_state["selected_option_group1_index"] = ["Báo cáo tỉ lệ bồi thường", "Báo cáo loại hình bồi thường", "Báo cáo theo quyền lợi","Báo cáo theo chi nhánh/Tập đoàn"].index(st.session_state["selected_option_group1"])
        st.write(f"Bạn đã chọn: **{st.session_state['selected_option_group1']}**")

    elif st.session_state["active_group"] == "group_2":
        st.session_state["selected_option_group2"] = st.selectbox(
            "Báo cáo y khoa/Nhân khẩu học",
            ["Báo cáo chuẩn đoán bệnh", "Báo cáo cơ sở y tế"],
            index=st.session_state.get("selected_option_group2_index", 0)
        )
        # Lưu lại lựa chọn
        st.session_state["selected_option_group2_index"] = ["Báo cáo chuẩn đoán bệnh", "Báo cáo cơ sở y tế"].index(st.session_state["selected_option_group2"])
        st.write(f"Bạn đã chọn: **{st.session_state['selected_option_group1']}**")
        
lua_chon = ''
if st.session_state['selected_option_group1'] == "Báo cáo tỉ lệ bồi thường" :
    lua_chon = 'Nhóm khách hàng'
elif st.session_state['selected_option_group1'] == "Báo cáo loại hình bồi thường" :
    lua_chon = 'Loại hình bồi thường'
elif st.session_state['selected_option_group1'] == "Báo cáo theo quyền lợi" :
    lua_chon = 'Nhóm quyền lợi'
elif st.session_state['selected_option_group1'] == "Báo cáo theo chi nhánh/Tập đoàn" :
    lua_chon = 'Đơn vị tham gia BH'
else:
    st.write("Vui lòng chọn nhóm phân tích")
    
    
# Hiển thị tiêu đề
st.markdown('<div class="title">CLAIM REPORT</div>', unsafe_allow_html=True)
st.title('')

# Load each file and display its data
dataframes = []
#df claim chungchung
for uploaded_file in uploaded_files:
    df = load_data(uploaded_file)
    
    if df is not None:
        if "fullerton" in uploaded_file.name.lower():
            df['Insured ID'] = df['Insured ID'].astype(str)
            fullerton_desired_columns = ['Insured ID',"Relation", 'Chan doan benh', 'Request amount','Claim amount','Rejected amount - paid case','Medical providers','Beneficiary type','Reject reasons','Client name','Policy effective date','Type of claim submit']
            df_fullerton_cleaned = df[fullerton_desired_columns]
            df_fullerton_cleaned.columns = ['Insured ID','Nhóm khách hàng', 'Nhóm bệnh', 'Số tiền yêu cầu bồi thường', 'Số tiền đã được bồi thường','Chênh lệch','Cơ sở y tế','Nhóm quyền lợi','Lý do từ chối','Đơn vị tham gia BH','Ngày hiệu lực','Loại hình bồi thường']
            df_fullerton_cleaned = df_fullerton_cleaned.reset_index(drop=True)
            dataframes.append(df_fullerton_cleaned) 
        # elif 'nhansu' in uploaded_file.name.lower():
#     df = df['Insured ID','Nhóm', 'Nhóm bệnh', 'Yêu cầu bồi thường', 'Đã được bồi thường','Chênh lệch','Cơ sở y tế','Nhóm quyền lợi','Lý do từ chối','Tên công ty']
        # else:
        #     # File không hợp lệ, xóa nó khỏi danh sách và cảnh báo
        #     st.error(f"Invalid file name: {uploaded_file.name}. This file does not match expected naming conventions.")
        #     uploaded_files.remove(uploaded_file)  # Xóa file không hợp lệ khỏi danh sách

if lua_chon in  ['Nhóm khách hàng','Loại hình bồi thường','Nhóm quyền lợi','Đơn vị tham gia BH']:
    option = lua_chon
    group = duckdb.sql(
        f"""
    SELECT 
        "{option}",
        count(distinct "Insured ID") as "Số người yêu cầu bồi thường",
        count("Insured ID") as "Số hồ sơ bồi thường",
        concat(round(count("Insured ID")*100 /count(*),1),'%') as "%Trường hợp",
        ROUND(SUM("Số tiền yêu cầu bồi thường")) AS "Số tiền yêu cầu bồi thường",
        ROUND(SUM("Số tiền đã được bồi thường")) AS "Số tiền được bồi thường",
        ROUND(SUM("Số tiền đã được bồi thường")/count(distinct "Insured ID")) as "Số tiền bồi thường trung bình/người",
        concat(round(SUM("Số tiền đã được bồi thường")*100/SUM("Số tiền yêu cầu bồi thường"),1),'%') as "Tỉ lệ thành công",
        datediff('day',STRPTIME(CAST("Ngày hiệu lực" AS VARCHAR), '%Y-%m-%d %H:%M:%S'), now()) as "Số ngày đã tham gia"
    FROM df_fullerton_cleaned
    GROUP BY "{option}","Ngày hiệu lực"
"""
    ).df()

    nhansu_file = None 
    for file in uploaded_files:
        if 'nhansu' in file.name.lower():  # Kiểm tra tên tệp có chứa 'nhansu'
            nhansu_file = file
            break
    if nhansu_file:
        nhansu_df = pd.read_csv(nhansu_file)
        result = pd.merge(group, nhansu_df, how='right', on='Insure ID')
        count = result.groupby('Insure ID')['Insure ID'].count().reset_index(name='Số người được bảo hiểm')
        sum_phi = result.groupby('Insure ID')['Phí baor hiểm'].sum().reset_index(name='Phí bảo hiểm')
        group.insert(1, 'Số người được bảo hiểm', count.pop('Số người được bảo hiểm'))
        group.insert(6, 'Phí bảo hiểm', count.pop('Phí bảo hiểm'))
        a = group["Số người yêu cầu bồi thường"] / group['Số người được bảo hiểm']
        group.insert(3, 'Tỉ lệ yêu cầu bồi thường', a )
        b = group["Số tiền được bồi thường"] * group["Số ngày đã tham gia"]/365*group["Phí bảo hiểm"]*100
        group.insert(11, 'Tỉ lệ loss thực tế', b)
        c = group["Số tiền được bồi thường"] * group["Số ngày đã tham gia"]/(365+30*2)*group["Phí bảo hiểm"]*100
        group.insert(122, 'Tỉ lệ loss ước tính (14m)', c)
    else:
group.insert(1, 'Số người được bảo hiểm', None)
        a = group["Số người yêu cầu bồi thường"] / group['Số người được bảo hiểm']
        group.insert(3, 'Tỉ lệ yêu cầu bồi thường', None)
        group.insert(6, 'Phí bảo hiểm', None)
        group.insert(11, 'Tỉ lệ loss thực tế', None)
        group.insert(12, 'Tỉ lệ loss ước tính (14m)', None)
        
    group_display = group.copy()
    def format_number(x):
        return "{:,.0f}".format(x)
    group_display['Số tiền yêu cầu bồi thường'] = group_display['Số tiền yêu cầu bồi thường'].apply(format_number)
    group_display['Số tiền được bồi thường'] = group_display['Số tiền được bồi thường'].apply(format_number)
    group_display['Số tiền bồi thường trung bình/người'] = group_display['Số tiền bồi thường trung bình/người'].apply(format_number)
    # Hàm để trang trí bảng
    def style_table(df):
        # Màu sắc cho hàng header
        styled_df = df.style.set_table_styles([{'selector': 'thead th', 'props': [('background-color', '#F1798B'), ('color', 'black')]},])
        
        # Màu sắc luân phiên cho các hàng còn lại
        def row_style(row):
            if row.name % 2 == 0:
                return ['background-color: #6C7EE1'] * len(row)  # Màu vàng nhạt cho hàng chẵn
            else:
                return ['background-color: #FFC4A4'] * len(row)  # Màu xanh biển đậm cho hàng lẻ
        
        styled_df = styled_df.apply(row_style, axis=1)  # Áp dụng màu cho từng hàng
        return styled_df
    # Hiển thị DataFrame đã trang trí trong Streamlit, với độ cao cuộn
    st.dataframe(style_table(group_display), height=250)
    
    top_5_case = group.sort_values(by='Số người yêu cầu bồi thường', ascending=False).head(5)
    top_5_amount = group.sort_values(by='Số tiền được bồi thường', ascending=False).head(5)
    col_pie_chart1, col_pie_chart2 = st.columns(2)
    with col_pie_chart1:
        pie_chart1 = px.pie(top_5_case, names=f'{lua_chon}', values="Số hồ sơ bồi thường", title=f'Số hồ sơ yêu cầu bồi thường theo {lua_chon.lower()}', 
            color=f'{lua_chon}',  
            color_discrete_map={
                "Dependant": "#3A0751", 
                "Employee": "#f2c85b"
            },  # Ánh xạ màu
            hole=0.6)
        st.plotly_chart(pie_chart1)
    with col_pie_chart2:
        pie_chart2 = px.pie(top_5_amount, names=f'{lua_chon}', values="Số tiền được bồi thường", title=f'Số tiền đã bồi thường theo {lua_chon.lower()}',hole=0.6)
        st.plotly_chart(pie_chart2)
#df demographicdemographic
for uploaded_file in uploaded_files:
    df = load_data(uploaded_file)
    if df is not None:
        if "fullerton" in uploaded_file.name.lower():
            try:
a1 = ['Insured ID','Request amount','Claim amount','Rejected amount - paid case','Gender',"DOBDOB"] 
                df_fullerton_demo = df[a1]  
                df_fullerton_demo.columns = ['Insured ID', 'Số tiền yêu cầu bồi thường', 'Số tiền đã được bồi thường','Chênh lệch','Giới tính','Ngày sinh']
                df_fullerton_demo = df_fullerton_cleaned.reset_index(drop=True)
            except KeyError as e:
                print(f"Lỗi: Cột {e} không tồn tại trong bảng.")
                
 

    
    
    
# demograph = ['Độ tuổi','Giới tính']
# for file in uploaded_files:
    
#     if 'nhansu' in file.name.lower():  # Kiểm tra tên tệp có chứa 'nhansu'
#             nhansu_file = file
#             break
#     if nhansu_file:
#         for 
#     else:
