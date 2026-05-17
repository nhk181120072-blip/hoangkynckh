import streamlit as st
import pandas as pd
import plotly.express as px

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Hoàng Kỳ TLU Portal", layout="wide")

# --- CUSTOM CSS ĐỂ GIAO DIỆN ĐẸP HƠN ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    
    section[data-testid="stSidebar"] {
        background-color: #005088 !important;
        color: white;
    }
    section[data-testid="stSidebar"] * { color: white !important; }

    .card-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin-top: 20px;
    }
    .card {
        background-color: #5da7db;
        border-radius: 15px;
        padding: 40px 20px;
        text-align: center;
        color: white;
        cursor: pointer;
        transition: 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .card:hover {
        transform: translateY(-5px);
        background-color: #005088;
    }
    .card i {
        font-size: 50px;
        margin-bottom: 15px;
    }
    .card h3 {
        margin: 0;
        font-size: 20px;
        font-weight: 500;
    }
    </style>
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    """, unsafe_allow_html=True)

# --- SIDEBAR: TẢI DỮ LIỆU ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/vi/8/82/Logo_Thuyloi_University.png", width=100)
    st.title("Hệ Thống Hoàng Kỳ TLU")
    st.markdown("---")
    
    # Nút tải file danh sách sinh viên
    uploaded_file = st.file_uploader("📂 Tải file Excel Sinh viên", type=["xlsx", "csv"])
    
    st.markdown("---")
    menu = ["🏠 Trang chủ", "📋 Điểm danh", "📚 Tài liệu", "🤖 Trợ lý AI", "📈 Tiến độ"]
    choice = st.radio("Điều hướng", menu)

# --- XỬ LÝ DỮ LIỆU EXCEL ---
# --- XỬ LÝ DỮ LIỆU EXCEL ---
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    
    # 1. Tự động chuẩn hóa tên cột (đề phòng file Excel viết thường 'mã sv', 'họ tên')
    rename_dict = {}
    for col in df.columns:
        if col.strip().lower() in ['mã sv', 'masv', 'mã sinh viên']:
            rename_dict[col] = 'Mã SV'
        elif col.strip().lower() in ['họ tên', 'hoten', 'họ và tên']:
            rename_dict[col] = 'Họ tên'
        elif col.strip().lower() == 'lớp':
            rename_dict[col] = 'Lớp'
    df = df.rename(columns=rename_dict)
    
    # 2. Tự động chèn thêm cột Điểm và Điểm danh nếu file Excel chưa có
    if "Điểm QT" not in df.columns:
        df["Điểm QT"] = 0.0  # Mặc định gán điểm 0 cho cả lớp
    if "Vắng" not in df.columns:
        df["Vắng"] = False   # Mặc định ban đầu là không ai vắng mặt

else:
    # Dữ liệu giả lập hiển thị khi chưa tải file
    df = pd.DataFrame({
        "STT": [1, 2, 3],
        "Mã SV": ["67KTS01", "67KTS02", "67KTS03"],
        "Họ tên": ["Nguyễn Văn A", "Trần Thị B", "Lê Văn C"],
        "Lớp": ["67KTS1", "67KTS1", "67KTS2"],
        "Điểm QT": [7.0, 8.5, 5.0],
        "Vắng": [False, True, False]
    })

# --- NỘI DUNG CHÍNH CHO TỪNG MODULE ---
if choice == "🏠 Trang chủ":
    st.title("Chào mừng đến với Hoàng Kỳ TLU")
    st.markdown(f"**Xin chào!** Hệ thống đã sẵn sàng với {len(df)} sinh viên.")
    
    st.markdown(f"""
        <div class="card-container">
            <div class="card"><i class="fa-solid fa-user-graduate"></i><h3>Thông tin sinh viên</h3></div>
            <div class="card"><i class="fa-solid fa-pen-to-square"></i><h3>Đăng ký học</h3></div>
            <div class="card"><i class="fa-solid fa-calendar-check"></i><h3>Kết quả học tập</h3></div>
            <div class="card"><i class="fa-solid fa-file-invoice-dollar"></i><h3>Học phí</h3></div>
            <div class="card"><i class="fa-solid fa-book"></i><h3>Chương trình đào tạo</h3></div>
            <div class="card"><i class="fa-solid fa-clock-rotate-left"></i><h3>Lịch thi</h3></div>
        </div>
    """, unsafe_allow_html=True)

elif choice == "📋 Điểm danh":
    st.header("📋 Quản lý Điểm danh & Nhập điểm")
    st.info("💡 Các cột STT, Mã SV, Họ tên, Lớp đã được khóa cố định. Thầy cô chỉ có thể nhập Điểm (0-10) và tích chọn Vắng mặt.")
    
    # Kiểm tra và đảm bảo cột "Vắng" có kiểu dữ liệu boolean (True/False)
    if "Vắng" in df.columns:
        df["Vắng"] = df["Vắng"].astype(bool)
    else:
        df["Vắng"] = False

    # Hiển thị bảng với các cấu hình khóa cột và chỉnh sửa giao diện cột
    edited_df = st.data_editor(
        df,
        disabled=["STT", "Mã SV", "Họ tên", "Lớp"],  # Khóa cứng 4 cột này
        column_config={
            "Vắng": st.column_config.CheckboxColumn(
                "Vắng mặt?",
                help="Tích vào ô này nếu sinh viên nghỉ học",
                default=False,
            ),
            "Điểm QT": st.column_config.NumberColumn(
                "Điểm Quá trình",
                help="Nhập điểm từ 0 đến 10",
                min_value=0.0,
                max_value=10.0,
                step=0.5,
                format="%.1f"
            )
        }, # <--- Lỗi của bạn nằm ở việc thiếu dấu ngoặc đóng } này
        use_container_width=True,
        hide_index=True,  
        num_rows="fixed"  
    ) # <--- Và thiếu cả dấu ngoặc đóng ) của hàm st.data_editor
    
    if st.button("💾 Lưu thay đổi"):
        st.success("Đã cập nhật dữ liệu thành công!")

elif choice == "📚 Tài liệu":
    st.header("📚 Thư viện Tài liệu & Quy chế")
    st.info("Hệ thống lưu trữ tài liệu nội bộ. Giảng viên có quyền tải lên, Sinh viên có quyền xem và tải xuống.")
    
    # 1. Giả lập phân quyền người dùng
    vai_tro = st.radio("Đóng vai người dùng:", ["Giảng viên", "Sinh viên"], horizontal=True)
    st.markdown("---")
    
    # 2. Tạo thư mục 'uploads' ngầm trong máy tính để cất file nếu chưa có
    import os
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
        
    col1, col2 = st.columns([1, 2])
    
    # 3. Khu vực tải file lên (Chỉ Giảng viên mới được dùng)
    with col1:
        st.subheader("Tải lên tài liệu")
        if vai_tro == "Giảng viên":
            doc_type = st.selectbox("Loại tài liệu", ["Bài giảng", "Quy chế", "Đề thi mẫu"])
            uploaded_doc = st.file_uploader("Chọn file", type=["pdf", "pptx", "docx", "xlsx"])
            
            if st.button("📤 Tải lên hệ thống"):
                if uploaded_doc is not None:
                    # Ghi file trực tiếp vào thư mục 'uploads' trên hệ thống
                    file_path = os.path.join("uploads", uploaded_doc.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_doc.getbuffer())
                    st.success(f"Đã lưu thành công: {uploaded_doc.name}")
                else:
                    st.warning("Vui lòng chọn file trước khi tải lên!")
        else:
            st.error("🔒 Tính năng bị khóa. Chỉ Giảng viên mới có quyền tải tài liệu lên hệ thống.")
            
    # 4. Khu vực xem và tải file xuống (Cả Giảng viên và Sinh viên đều thấy)
    with col2:
        st.subheader("Danh sách tài liệu đã lưu")
        # Quét thư mục 'uploads' xem đang có những file nào
        saved_files = os.listdir("uploads")
        
        if len(saved_files) == 0:
            st.write("📂 Chưa có tài liệu nào trên hệ thống.")
        else:
            # Tạo nút tải xuống cho từng file có trong thư mục
            for file_name in saved_files:
                file_path = os.path.join("uploads", file_name)
                with open(file_path, "rb") as f:
                    file_bytes = f.read()
                    
                st.download_button(
                    label=f"⬇️ Tải file: {file_name}",
                    data=file_bytes,
                    file_name=file_name,
                    mime="application/octet-stream"
                )

elif choice == "🤖 Trợ lý AI":
    st.header("🤖 Trợ lý AI Cố vấn Học tập (Real-time AI)")
    st.info("🚀 Hệ thống sử dụng hạ tầng LPU của Groq để phản hồi siêu tốc.")
    
    # CHỈ SỬA KHÚC NÀY: Lấy key bảo mật từ Streamlit Secrets thay vì dùng st.text_input
    groq_key = st.secrets.get("GROQ_API_KEY") if "GROQ_API_KEY" in st.secrets else None
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Hỏi AI bất cứ điều gì..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            if groq_key:  # Nếu đã cấu hình key ngầm thành công
                try:
                    from groq import Groq
                    client = Groq(api_key=groq_key)  # Truyền key bí mật vào đây
                    
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "system",
                                "content": "Bạn là Trợ lý Cố vấn Học tập của trường Đại học. Trả lời bằng tiếng Việt, ngắn gọn, súc tích và chuyên nghiệp."
                            },
                            {
                                "role": "user",
                                "content": prompt,
                            }
                        ],
                        model="llama-3.1-8b-instant",
                    )
                    reply = chat_completion.choices[0].message.content
                except Exception as e:
                    reply = f"❌ Lỗi kết nối AI: {str(e)}"
            else:
                reply = "⚠️ Lỗi: Hệ thống chưa được cấu hình API Key bảo mật. Vui lòng kiểm tra lại thiết lập App Secrets."
            
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
elif choice == "📈 Tiến độ":
    st.header("📈 Cố vấn Học tập & Dự báo kết quả")
    
    # Tạo các Tab để giao diện gọn gàng hơn
    tab1, tab2, tab3 = st.tabs(["🎯 Mục tiêu Môn học", "📊 Quản lý GPA", "⚠️ Cảnh báo Học thuật"])

    with tab1:
        st.subheader("Tính điểm thi để đạt hạng (A, B, C)")
        col_a, col_b = st.columns(2)
        
        with col_a:
            diem_qt = st.number_input("Nhập điểm Quá trình (10):", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
            he_so_qt = st.slider("Hệ số điểm Quá trình (%):", 10, 50, 40) / 100
            he_so_thi = 1 - he_so_qt
            
        with col_b:
            st.markdown(f"**Cơ chế tính:** QT({he_so_qt*100:.0f}%) + Thi({he_so_thi*100:.0f}%)")
            
            # Hàm tính điểm cần thiết
            def tinh_diem_can(target_score, qt, hs_qt, hs_thi):
                needed = (target_score - (qt * hs_qt)) / hs_thi
                return needed if needed <= 10 else "Không thể đạt"

            # Bảng mục tiêu (Theo thang điểm Thủy Lợi/NEU thông thường)
            targets = {"Điểm A (8.5)": 8.5, "Điểm B (7.0)": 7.0, "Điểm C (5.5)": 5.5}
            
            for label, score in targets.items():
                needed = tinh_diem_can(score, diem_qt, he_so_qt, he_so_thi)
                if isinstance(needed, float):
                    if needed < 0:
                        st.success(f"✅ **{label}:** Đã đủ điểm (Cần thi {max(0.0, needed):.2f})")
                    else:
                        st.info(f"📝 **{label}:** Cần thi **{needed:.2f}** điểm")
                else:
                    st.error(f"❌ **{label}:** {needed}")

    with tab2:
        st.subheader("Theo dõi lộ trình GPA")
        # Giả lập bảng điểm tổng hợp các môn
        data_gpa = pd.DataFrame({
            "Môn học": ["Kinh tế số", "Luật kinh tế", "Lập trình Python", "Marketing", "Kế toán"],
            "Số tín chỉ": [3, 2, 3, 3, 2],
            "Điểm số": [8.5, 7.0, 9.0, 6.5, 8.0]
        })
        
        edited_gpa = st.data_editor(data_gpa, num_rows="dynamic", use_container_width=True)
        
        # Tính toán GPA (Thang 4)
        def convert_to_4(x):
            if x >= 8.5: return 4.0
            if x >= 7.0: return 3.0
            if x >= 5.5: return 2.0
            if x >= 4.0: return 1.0
            return 0.0

        edited_gpa['Điểm hệ 4'] = edited_gpa['Điểm số'].apply(convert_to_4)
        total_tc = edited_gpa['Số tín chỉ'].sum()
        total_score = (edited_gpa['Điểm hệ 4'] * edited_gpa['Số tín chỉ']).sum()
        current_gpa = total_score / total_tc if total_tc > 0 else 0
        
        st.metric("GPA Hiện tại (Thang 4)", f"{current_gpa:.2f}")

    with tab3:
        st.subheader("🎯 Đặt mục tiêu & Cảnh báo rủi rơ")
        target_gpa = st.slider("Mục tiêu GPA của bạn (Thang 4):", 1.0, 4.0, 3.2, step=0.1)
        
        # Logic cảnh báo
        if current_gpa < 2.0:
            st.error("🚨 **CẢNH BÁO ĐUỔI HỌC:** GPA của bạn đang dưới 2.0. Hệ thống đề xuất gặp Cố vấn học tập ngay lập tức!")
        elif current_gpa < target_gpa:
            st.warning(f"⚠️ **DƯỚI MỤC TIÊU:** Bạn còn thiếu {target_gpa - current_gpa:.2f} điểm nữa để đạt mục tiêu {target_gpa}. Hãy tập trung cải thiện các môn 3 tín chỉ.")
        else:
            st.balloons()
            st.success(f"🌟 **VƯỢT MỤC TIÊU:** Tuyệt vời! Bạn đang duy trì phong độ rất tốt.")

        # Biểu đồ dự báo
        st.markdown("---")
        fig_gpa = px.line(edited_gpa, x="Môn học", y="Điểm số", title="Biến động phong độ học tập", markers=True)
        st.plotly_chart(fig_gpa, use_container_width=True)
