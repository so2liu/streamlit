import streamlit as st
import pandas as pd
import os
import base64
import chardet

from llm import AI


def show_image(base64code: str):
    """Show image from base64 code"""
    if ',' in base64code:
        data = base64code.split(',')[1]
    else:
        data = base64code
    binary = base64.b64decode(data)
    st.image(binary, use_column_width=True)


ai = None
# input for openai-key
openai_key = st.text_input('OpenAI Key', value='',
                           type='password', help="回车确认")
if openai_key:
    hiddened_key = openai_key[:4] + '*' * \
        (len(openai_key) - 8) + openai_key[-4:]
    st.write(f"OpenAI Key: {hiddened_key}")
    ai = AI(openai_key)

# select model
model_type = st.selectbox('模型类型', ['gpt3_5', 'gpt4'])
if ai is not None:
    ai.set_config(model_type)

# upload excel or csv file
uploaded_file = st.file_uploader("上传文件", type=["csv", "xls", "xlsx"])
if uploaded_file is not None:
    match uploaded_file.name.split('.')[-1]:
        case 'xlsx' | 'xls':
            df = pd.read_excel(uploaded_file)
        case 'csv':
            filepath = os.path.join('./uploads', uploaded_file.name)
            with open(filepath, 'wb') as f:
                f.write(uploaded_file.getbuffer())

            result = chardet.detect(uploaded_file.read())
            encoding = result['encoding']
            df = pd.read_csv(filepath, encoding=encoding)
        case _:
            raise ValueError('文件格式错误')

    if ai is not None:
        ai.load_df(df)
    st.write(df)

# ask a question and get a chart
question = st.text_input('问题', value='')
chart_type = st.selectbox('图表类型', ['柱状图', '折线图', '散点图', '饼图', '箱线图', '热力图'])
if question:
    charts = ai.ask_question(question, visualization=chart_type)

button = st.button('生成报告', type='primary')
if button:
    data = charts[0].raster
    show_image(data)

# edit report
edit_advice = st.text_area('修改建议', value='', placeholder='请在此处输入编辑建议，每行一条')
if edit_advice:
    instructions = edit_advice.split('\n')
    try:
        charts = ai.edit_chart(
            instructions=instructions, code=charts[0].code, library='seaborn')
        show_image(charts[0].raster)
    except Exception as e:
        st.write(e)
