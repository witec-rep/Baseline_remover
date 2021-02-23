from BaselineRemoval import BaselineRemoval

import pandas as pd
import base64

import streamlit as st
import zipfile
from bokeh.plotting import figure
from bokeh.palettes import all_palettes
colori = all_palettes['Category20'][20]

@st.cache(allow_output_mutation=True)
def load_func(uploadfile):
    zf = zipfile.ZipFile(uploadfile)
    files = dict()
    for i, name in enumerate(zf.namelist()):
        files[name] = pd.read_csv(zf.open(name), header = None, sep = '\t')
    return files, zf.namelist()

def download_file(data, filename):
    testo = 'Download '+filename+'.csv'
    csv = data.to_csv(index=False, header = None, sep = ' ')
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">'+testo+'</a>'
    st.markdown(href, unsafe_allow_html=True)

st.subheader('The files loaded need to be in a specific shape:')
st.subheader(' - 3 columns, the first one with the X coordinates')
st.subheader(' - the second one as dummy column (could be filled with random numbers does not matter)')
st.subheader(' - the third one with the Y values')
uploadfile = st.file_uploader('load zip file here', 'zip')

if uploadfile:
    files, files_names = load_func(uploadfile)

    for file in files:
        #baseline removal:
        baseObj=BaselineRemoval(files[file][2])
        Zhangfit_output=baseObj.ZhangFit()
        files[file][3] = Zhangfit_output

    name = st.selectbox('Select spectrum:', files_names)

    p1 = figure(title='', x_axis_label='', y_axis_label='')#, x_axis_type = scale_logx, y_axis_type = scale_logy)
    p1.line(files[name][0], files[name][2], line_width=2, color = colori[1])
    p1.line(files[name][0], files[name][2]-files[name][3], line_width=2, color = colori[0])
    st.bokeh_chart(p1, use_container_width=True)

    p1 = figure(title='', x_axis_label='', y_axis_label='')#, x_axis_type = scale_logx, y_axis_type = scale_logy)
    p1.line(files[name][0], files[name][3], line_width=2)
    st.bokeh_chart(p1, use_container_width=True)

    for namei in files_names:
        download_file(files[namei], namei)
