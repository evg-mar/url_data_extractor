import os, re, csv, datetime
import pandas as pd
from dotenv import load_dotenv
import json

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

from front_end.htmlTemplates import css

from llm_extraction import extract_furniture_products
from llm_connector import get_llm_openai
from util_extraction import get_raw_after_products

import streamlit as st
import streamlit_agraph as agraph

from langchain.prompts.prompt import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.llm import LLMChain



st.set_page_config(page_title="Furniture extractor",
                    page_icon = "./front_end/images/furniture_extraction.jpg",
                    layout='wide')

st.write(css, unsafe_allow_html=True)



def main():

    st.markdown("### Extract furniture information from URL")

    load_dotenv()



    with st.sidebar:
        st.sidebar.image("./front_end/images/furniture_extraction.jpg")
        st.header("AI data extractor")

    st.session_state.chain_extract = extract_furniture_products(llm = get_llm_openai())

    button01 = st.button("Show extracted data from CSV")
    if button01:
        st.write("Extracted data from CSV file:")
        db_csv_path = os.getenv('DB_EXTRACTED_CSV')
        st.session_state.df_data_extracted = pd.read_csv(db_csv_path, 
                                            # index_col='index',
                                           usecols=['URL', 'domain', 'raw_text',
                                                    'furniture_extr','property_extr','name_extr'])
    if button01 or 'df_data_extracted' in st.session_state:    
        st.dataframe(st.session_state.df_data_extracted)
        
        tab_wordcloud, tab_histogram = st.tabs(['Word Cloud', 'Word Count'])

        with tab_wordcloud:
            if 'wordcloud' not in st.session_state:
                text_values = st.session_state.df_data_extracted['furniture_extr'].values
                text_list = [str(val) for val in text_values if isinstance(val, str)]
                text = ', '.join(text_list)
                st.session_state.text_list = text_list
                st.session_state.wordcloud = WordCloud().generate(text)

            fig, ax = plt.subplots(figsize=(10, 8))
            ax.imshow(st.session_state.wordcloud, interpolation='bilinear', 
                    #   aspect='auto'
                      )
            # tight_layout()

            # plt.imshow(st.session_state.wordcloud, interpolation='bilinear')
            ax.axis("off")
            # plt.show()
            st.pyplot(fig)
        
        with tab_histogram:
            word_list = st.session_state.text_list

            # counts = Counter(word_list)
            counts = dict(Counter(word_list).most_common(45))

            labels, values = zip(*counts.items())

            # sort your values in descending order
            indSort = np.argsort(values)[::-1]

            # rearrange your data
            labels = np.array(labels)[indSort]
            values = np.array(values)[indSort]

            indexes = np.arange(len(labels))

            bar_width = 0.35

            fig, ax = plt.subplots(figsize=(12,8))
            
            ax.bar(indexes, values)

            # add labels
            # ax.set_xticks(indexes + bar_width)
            ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=5)
            ax.set(xticks=indexes + bar_width)
            plt.rc('ytick', labelsize=5) 
            # ax.yaxis.label.set_size(15)
            # ax.xaxis.label.set_size(15)
            # plt.show()
            
            # ax.hist(arr, bins=20)

            st.pyplot(fig)


    with st.sidebar:
        with st.form("extract information"):
            if 'url_query' not in st.session_state:
                st.session_state.url_query = ""
            value_url = "" if 'url_query' not in st.session_state \
                        else st.session_state.url_query
            url_query = st.text_area(":auto[Input a URL:]", 
                                    #  height=50,
                    value = value_url,
                    placeholder='https://interiorsinvogue.com/products/side-sofa-table-silver-finish-har189sadf')
            url_query = url_query.strip()
            submitted_btn = st.form_submit_button("Query preprocessing")
            if submitted_btn: # and st.session_state.vars['user_query_kbg'].status==VariableStatus.Changed:
                url_query = url_query.strip()
                if url_query != st.session_state.url_query:
                    st.session_state.url_query = url_query 
                                            
                query_preprocessed = get_raw_after_products(st.session_state.url_query)
                if 'query_preprocessed' not in st.session_state:
                    st.session_state.query_preprocessed = query_preprocessed
                if query_preprocessed != st.session_state.query_preprocessed:
                    st.session_state.query_preprocessed = query_preprocessed

                # st.write("Preprocessed query:")
                # st.write(f":blue[**{query_preprocessed}**]")

            query_preprocessed = "" \
                    if 'query_preprocessed' not in st.session_state \
                    else st.session_state.query_preprocessed

            query_preprocessed = st.text_area(":auto[Preprocessed URL query:]", 
                                    #   height=40,
                                        value=query_preprocessed,
                                        # placeholder='side sofa table silver'
                                        )
            
            submitted_prep = st.form_submit_button("Extract data")
            if submitted_prep: # and st.session_state.vars['user_query_kbg'].status==VariableStatus.Changed:
                query_preprocessed = query_preprocessed.strip() if query_preprocessed is not None else ''
            
                result = \
                    st.session_state.chain_extract(query_preprocessed)
                
                text = result['text']
                st.session_state.text_json = json.loads(text)

                st.write("Extracted data:")
                st.write(st.session_state.text_json)

main()
# if __name__ == "__main__":
#     main()

