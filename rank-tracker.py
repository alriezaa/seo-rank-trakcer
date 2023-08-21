import pandas as pd
import requests
import json
import ast
import streamlit as st

super_dev_url="https://serper.dev/signup"
linkedin="https://linkedin.com/in/alirezaa"
st.title("Rank Tracker project")
st.markdown("follow alireza heidari on [linkedin](%s)" % linkedin )


st.subheader("Start Using Rank Tracker")
api_key=st.text_input("Insert the api_key: ")
st.write("sign up in [link](%s) for get api key" % super_dev_url)
st.write("--------------------------------------------------------------------")
keyword_csv_file=st.file_uploader("please upload your csv file with keyword column",type=['csv','xlsx'],accept_multiple_files=False)
st.write("--------------------------------------------------------------------")
website=st.text_input("Insert the website without http or https: ")
st.write("--------------------------------------------------------------------")

final_data=[]
if api_key and keyword_csv_file and website:
    with st.spinner("Please wait..."):
        keyword_df=pd.read_csv(keyword_csv_file)
        test_url = "https://google.serper.dev/search"
        test_payload = json.dumps({
                "q":"ورزش ۳",
                "gl": "ir",
                "num": 100   
        })
        test_headers = {
                'X-API-KEY': api_key,
                'Content-Type': 'application/json'
        }
        test_response = requests.request("POST",test_url, headers=test_headers, data=test_payload).text
        if "Your client does not have permission to get URL" in test_response:
            st.write("403 forbidden , please use another vpn")
        else:
            for i in range (keyword_df.shape[0]):
                url = "https://google.serper.dev/search"
                payload = json.dumps({
                    "q":keyword_df.loc[i,"keyword"],
                    "gl": "ir",
                    "num": 100   
                })
                headers = {
                    'X-API-KEY': api_key,
                    'Content-Type': 'application/json'
                }
                response = requests.request("POST", url, headers=headers, data=payload).text


                serp_data=(ast.literal_eval(response))["organic"]
                website_page="not found"
                website_position="not found"
                website_title="not found"
                for j in range(len(serp_data)):
                    if website in serp_data[j]["link"]:
                        website_page=serp_data[j]["link"]
                        website_position=serp_data[j]["position"]
                        website_title=serp_data[j]["title"]
                        break
                raw_data=[keyword_df.loc[i,"keyword"],website_position,website_title,website_page]
                final_data.append(raw_data)
            final_df=pd.DataFrame(final_data,columns=["keyword","rank","title","url"])
            st.write(final_df)
            st.download_button(label="download rank data as csv",data=final_df.to_csv(),file_name="rank_keyword_tracker.csv",mime='text/csv')
        
        
            
            
                    
        