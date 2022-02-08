import streamlit as st
import pandas as pd
import numpy as np
import requests

st.title('Google Search Keywords Clustering')

st.header('Step 1: Upload Keywords as CSV')
uploaded_csv = st.file_uploader('Upload Keywords CSV file', type='csv', help='Required cols: Keyword, Avg. monthly searches')

btn_send_csv = st.button('Upload CSV for clustering')

requestid = ''

if btn_send_csv:
    if uploaded_csv is not None:

        url = "http://gsearch-ai.ap-south-1.elasticbeanstalk.com/cluster/api"

        payload={'brand_name': 'foodpanda',
        'cluster_sensitivity': 'HIGH',
        'competitors': '["swiggy","zomato"]'}
        files=[
        ('keyword_file',(uploaded_csv.name, uploaded_csv,'text/csv'))
        ]
        headers = {
        'x-api-key': 'SRA3FCn8.38uqbtRNg7tMigbBkHFfK5G0t3GIF30F'
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        st.write('status: ' + response.json()['status'])
        st.write('requestid: ' + response.json()['requestid'])

        requestid = response.json()['requestid']
                
    else:
        st.write('Upload CSV to begin.')


st.header('Step 2: Get cluster result for given Request Id')

in_requestid = st.text_input('Request Id')
btn_get_clusters = st.button('Get clusters for requestid')

if btn_get_clusters:
    if not in_requestid:
        st.write('Upload CSV to being, or enter requestid')
    else:
        url = "http://gsearch-ai.ap-south-1.elasticbeanstalk.com/cluster/status/api?request_ids=" + in_requestid

        headers = {
        'x-api-key': 'SRA3FCn8.38uqbtRNg7tMigbBkHFfK5G0t3GIF30F'
        }

        response = requests.request("GET", url, headers=headers)
        t_status = response.json()['status_list'][0]['status']
        st.write('Status: ' + t_status)
        if t_status == 'processing':
            st.write('Request in process, please try again in few moments')
        else:
            st.write('File URL: ' + response.json()['status_list'][0]['result_file_url'].replace('.json', '.csv') )