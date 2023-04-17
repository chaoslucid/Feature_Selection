import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import seaborn as sns

font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
plt.rcParams['font.family'] = ['SimHei']
# 设置页面标题
st.set_page_config(page_title='半导体器件参数变化量计算工具')

# 设置页面标题和页面描述
st.title('半导体器件参数变化量计算工具')
st.write('输入两个存储元器件测试结果的excel文件，分别为试验前和试验后，手动导入数据后展示数据，然后选择参数列（可多选），用试验后的数据减去对应的试验前数据，得到变化量，并可视化变化量分布，展示数据')
# @st.cache(allow_output_mutation=True)
# 获取文件上传的函数
# def get_file():
#     uploaded_file = st.file_uploader("上传文件", type=["xlsx"])
#     if uploaded_file is not None:
#         return pd.read_excel(uploaded_file, engine='openpyxl')

# 获取用户选择的参数列的函数
def get_columns(df):
    # 选取所有数值类型的列
    columns = df.select_dtypes(include=np.number).columns.tolist()
    # 在页面上显示可供选择的列
    selected_columns = st.multiselect('选择参数列', columns)
    return selected_columns

# 计算变化量的函数
def calculate_changes(df1, df2, columns):
    changes = df2[columns] - df1[columns]
    return changes

# 可视化变化量分布的函数
# def plot_changes(x, fig, ax):
    
    # fig, ax = plt.subplots()
    # ax.hist(x)
    # ax.set_xlabel('变化量')
    # ax.set_ylabel('频率')
    # st.pyplot(fig)
   

# 页面交互逻辑
    
file1 = st.file_uploader("上传试验前的数据文件", type=["xlsx"])
file2 = st.file_uploader("上传试验后的数据文件", type=["xlsx"])


if file1 is not None and file2 is not None:
    f1=pd.read_excel(file1)
    f2=pd.read_excel(file2)
    st.write('试验前数据：')
    st.write(f1)
    st.write('试验后数据：')
    st.write(f2)
    columns = get_columns(f1)
    
    changes = calculate_changes(f1, f2, columns)
 
       
    st.write('变化量：')
    st.write(changes,width=800, height=800)
    # st.write(columns)
    # st.write(changes.shape[1])
    if columns:
        if changes.shape[1]==1:
           fig, ax= plt.subplots( figsize=(20, 10))
           # sns.histplot(changes, kde=True)
           sns.histplot(f1[columns[0]], kde=True,ax=ax)
           sns.histplot(f2[columns[0]], kde=True,ax=ax)
           # sns.histplot([f1[columns[0]], f2[columns[0]]], kde=True,ax=ax,multiple='stack')
           ax.set_xlabel(changes.columns[0])
        else:
       
            fig, axs= plt.subplots(nrows=changes.shape[1], figsize=(20, 20))
            # st.write(range(changes.shape[1]))
            # st.write(changes.iloc[:,0])
           
            # st.write(axs[1])
            for i in range(changes.shape[1]):
                # st.write(type([pd.DataFrame([f1[columns].iloc[:,i],f2[columns].iloc[:,i]])                             
                sns.histplot(f1[columns].iloc[:,i], ax=axs[i], kde=True)
                sns.histplot(f2[columns].iloc[:,i], ax=axs[i], kde=True)
                axs[i].set_xlabel(changes.columns[i])
                
            # for axi, col in zip(  ax, changes.columns):
            #     sns.histplot(changes[col], ax=axi, kde=True)
            #     axi.set_xlabel(col)
            
        st.pyplot(fig)