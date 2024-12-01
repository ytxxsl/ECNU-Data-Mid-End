import streamlit as st
import pandas as pd
import os

# 配置：每列独立的文件目录
DATA_DIRS = {
    "ODS 贴源数据层": "./pages/ODS",  # 替换为你的列1数据文件夹路径
    "DWD 明细数据层": "./pages/DWD",  # 替换为你的列2数据文件夹路径
    "ADS 应用数据层": "./pages/ADS",  # 替换为你的列3数据文件夹路径
}

# 获取指定目录中的表名
def get_table_names(data_dir):
    if os.path.exists(data_dir):
        return [f.replace(".pickle", "") for f in os.listdir(data_dir) if f.endswith(".pickle")]
    else:
        st.error(f"os.path.exists(data_dir) = {os.path.exists(data_dir)}")
        return []

# 加载表数据
def load_table_data(data_dir, table_name):
    file_path = os.path.join(data_dir, f"{table_name}.pickle")
    if os.path.exists(file_path):
        df = pd.read_pickle(file_path)
        return df.head(100)
    else:
        st.error(f"文件 {file_path} 不存在！")
        return None

# 主程序
st.title("中台数据架构")

# 初始化状态：保存选中表的信息
if "selected_table" not in st.session_state:
    st.session_state.selected_table = None
    st.session_state.selected_column = None

# 分为三列
cols = st.columns(3)

# 每列显示表名
for col_name, data_dir in zip(DATA_DIRS.keys(), DATA_DIRS.values()):
    with cols[list(DATA_DIRS.keys()).index(col_name)]:
        st.subheader(col_name)
        table_names = get_table_names(data_dir)
        for table_name in table_names:
            if st.button(table_name, key=f"{col_name}_{table_name}"):  # 添加按钮点击事件
                st.session_state.selected_table = table_name
                st.session_state.selected_column = col_name

# 底部显示选中的表数据
if st.session_state.selected_table and st.session_state.selected_column:
    st.divider()
    st.write(f"**查看数据：{st.session_state.selected_column} - {st.session_state.selected_table}**")
    st.write("仅采样100行数据")
    data_dir = DATA_DIRS[st.session_state.selected_column]
    data = load_table_data(data_dir, st.session_state.selected_table)
    if data is not None:
        st.dataframe(data)
