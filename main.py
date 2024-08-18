import streamlit as st
import json
# from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm
from vnstock import *

# start with wide mode
st.set_page_config(layout="wide")

st.image('https://vnstocks.com/img/vnstock_logo_trans_rec_hoz.png', width=120)
st.header("Thư viện mẫu Streamlit Web App cho người mới bắt đầu")

# Create 3 tabs
screener, help, credit = st.tabs(["Bộ lọc cổ phiếu", "Hướng dẫn", "Giới thiệu"])


default_query = {"exchangeName": "HOSE,HNX,UPCOM",
            "marketCap": (100, 1000)}

@st.cache_data
def tcbs_screener(query, limit=1700):
    screener_df = stock_screening_insights (query, size=limit, drop_lang='en')
    return screener_df

def pygwalker_part (df):
    # Initialize pygwalker communication
    init_streamlit_comm()
    renderer = StreamlitRenderer(df, spec="./gw_config.json", debug=False)
    renderer.render_explore()

# Define the content of each tab
with screener:
    st.markdown("## Bộ lọc cổ phiếu")

    # define 3 columns with equally width
    col1, col2, col3 = st.columns([1.5, 1, 1])
    with col1:
        # allow user to select exchange from HOSE, HNX, UPCOM
        exchange = st.multiselect("Sàn giao dịch", ["HOSE", "HNX", "UPCOM"], default=["HOSE", "HNX", "UPCOM"])
    with col2:
        # allow user to input market cap range
        market_cap = st.slider("Vốn hóa thị trường", 0, 10000, (100, 1000))
    with col3:
        # show a number input to define the limit of the result
        limit = st.number_input("Số lượng cổ phiếu tối đa", min_value=10, max_value=2000, value=1700)
    
    # update the query with the user input
    query = {"exchangeName": ",".join(exchange),
            "marketCap": market_cap}
    # call the function to get the result
    screener_df = tcbs_screener(query, limit)
    # show the result in a table
    st.write(screener_df)

    # st.markdown('## Khám phá')
    # pygwalker_part (screener_df)


with help:
    st.markdown("## Hướng dẫn")
    help_details = """
    ## Sử dụng Streamlit Cloud
    1. Tạo Github repository bằng cách folk repo này trên Github hoặc tạo mới một repo và copy toàn bộ nội dung trong thư mục repo này vào.
    2. Truy cập Streamlit Cloud (cần đăng ký mới nếu chưa có tài khoản tại: https://share.streamlit.io). Bạn có thể đăng nhập bằng tài khoản Github hiện có.
    3. Tạo ứng dụng mới trên Streamlit Share bằng cách chọn New app > Use existing repo và chọn repo bạn chuẩn bị sẵn trên Github
    ![](./assets/images/streamlit_cloud_setup_new_repo_thinhvu_vnstock_learn-anything.png)
    ## Sử dụng Hugging Face Spaces
    1. Tạo tài khoản Hugging Face tại: https://huggingface.co
    2. Truy cập Hugging Face Spaces tại: https://huggingface.co/new-space để tạo một không gian mới
    3. Đặt tên url cho không gian của bạn, ví dụ `vnstock-app`
    4. Chọn Space SDK là Streamlit
    5. Chọn chế độ chia sẻ công khai (Public) hay riêng tư (Private)
    6. Chọn Create Space để hoàn tất.
    7. Truy cập tab `Files` và chọn nút (button) `Upload files` để tải lên toàn bộ nội dung trong thư mục repo này.
    """
    st.markdown(help_details)

with credit:
    credit_details = """
    ## Giới thiệu
    
    Đây là mẫu Web App đơn giản minh họa cho người mới làm quen với việc xây dựng Data app trên nền tảng Web bằng streamlit trong Python.

    ## Tác giả
    * Tác giả: [Thinh Vu](https://thinhvu.com) @ vnstock.site
    * Email: support@vnstock.site
    * Website: [vnstock.site](https://vnstock.site)
    * Bạn có thể gửi tặng tác giả Cafe qua QR thay lời cảm ơn. Chi tiết [tại đây](https://docs.vnstock.site/community/tai-tro-du-an-vnstock/)    
    """
    st.markdown(credit_details)
