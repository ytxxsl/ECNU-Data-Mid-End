import streamlit as st
import pandas as pd
import os

# 配置：每列独立的文件目录
DATA_DIRS = {
    "列1": "./data1",  # 替换为你的列1数据文件夹路径
    "列2": "./data2",  # 替换为你的列2数据文件夹路径
    "列3": "./data3",  # 替换为你的列3数据文件夹路径
}

# 定义第二列的表与第一列表的关系
table_relationship = {
    "列2": {
        "tableA": ["table1", "table2"],  # tableA 与 table1 和 table2 相关联
        "tableB": ["table4", "table3"],  # tableB 与 table2 和 table3 相关联
    },
    "列3": {
        "table1_A": ["tableA", "tableB"],  # tableA 与 table1 和 table2 相关联
        "table2_B": ["tableB", "tableC"],  # tableB 与 table2 和 table3 相关联
    }
}

# 获取指定目录中的表名
def get_table_names(data_dir):
    if os.path.exists(data_dir):
        return [f.replace(".csv", "") for f in os.listdir(data_dir) if f.endswith(".csv")]
    else:
        return []

# 加载表数据
def load_table_data(data_dir, table_name):
    file_path = os.path.join(data_dir, f"{table_name}.csv")
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df.head(100)
    else:
        st.error(f"文件 {file_path} 不存在！")
        return None

# 主程序
st.title("多列独立表数据查看器")

# 初始化状态：保存选中表的信息
if "selected_table" not in st.session_state:
    st.session_state.selected_table = None
    st.session_state.selected_column = None
    st.session_state.related_tables = []

# 分为三列
cols = st.columns(3)

# 第一列：展示表名并动态更新样式
with cols[0]:
    st.subheader("列1")
    for table_name in get_table_names(DATA_DIRS["列1"]):
        is_related = table_name in st.session_state.related_tables
        button_label = f"➡ {table_name}" if is_related else table_name
        if st.button(button_label, key=f"col1_{table_name}"):
            st.session_state.selected_table = table_name
            st.session_state.selected_column = "列1"
            st.session_state.related_tables = []  # 点击第一列时清空关联状态

# 第二列：展示表名并设置关系
with cols[1]:
    st.subheader("列2")
    for table_name in get_table_names(DATA_DIRS["列2"]):
        is_related = table_name in st.session_state.related_tables
        button_label = f"➡ {table_name}" if is_related else table_name
        if st.button(button_label, key=f"col2_{table_name}"):
            st.session_state.selected_table = table_name
            st.session_state.selected_column = "列2"
            st.session_state.related_tables = table_relationship["列2"].get(table_name, [])

# 第三列：展示表名
with cols[2]:
    st.subheader("列3")
    for table_name in get_table_names(DATA_DIRS["列3"]):
        if st.button(table_name, key=f"col3_{table_name}"):
            st.session_state.selected_table = table_name
            st.session_state.selected_column = "列3"
            st.session_state.related_tables = table_relationship["列3"].get(table_name, [])  # 第三列无关联，清空高亮状态

# 底部显示选中的表数据
if st.session_state.selected_table and st.session_state.selected_column:
    st.divider()
    st.write(f"**当前选择：{st.session_state.selected_column} - {st.session_state.selected_table}**")
    data_dir = DATA_DIRS[st.session_state.selected_column]
    data = load_table_data(data_dir, st.session_state.selected_table)
    if data is not None:
        st.dataframe(data)
