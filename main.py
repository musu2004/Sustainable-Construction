import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit page layout
st.set_page_config(page_title="Sustainable Construction Dashboard", layout="wide")

# Apply custom CSS for enhanced UI
st.markdown(
    """
    <style>
    .drag-drop-area {
        border: 2px dashed #5A5A5A;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        background-color: #1E1E1E;
        color: white;
        margin-bottom: 20px;
    }
    .drag-drop-area:hover {
        border-color: #FF4B4B;
    }
    .dashboard-container {
        background-color: #232323;
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Full-page layout
header = st.container()
left_col, right_col = st.columns([1, 2])  # Adjust column proportions

# Header Section
with header:
    st.title("📊 Sustainable Construction Dashboard")
    st.caption("Upload any CSV or Excel file to analyze and visualize your data dynamically.")

# Left Column: File Upload Section
with left_col:
    st.subheader("Upload Your File")
    st.markdown('<div class="drag-drop-area">📥 Drag and drop your CSV or Excel file here</div>', unsafe_allow_html=True)

    # File uploader
    uploaded_file = st.file_uploader("", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            # Load data depending on file type
            if uploaded_file.name.endswith(".csv"):
                data = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".xlsx"):
                data = pd.read_excel(uploaded_file)
            else:
                data = None

            if data is None or data.empty:
                st.warning("The uploaded file is empty or unsupported. Please upload a valid CSV or Excel file.")
            else:
                # Preview the first few rows of the data
                st.write("Uploaded Data Preview:")
                st.dataframe(data.head(), use_container_width=True)

                # Option to show full data
                if st.checkbox("🔍 Show Full Data"):
                    st.write(data)
        except Exception as e:
            st.error(f"Error reading file: {e}")
    else:
        st.info("Please upload a CSV or Excel file to continue.")

# Right Column: Dynamic Dashboard
if uploaded_file and not data.empty:
    with right_col:
        st.subheader("Dashboard")

        # Key insights (only numeric columns)
        numeric_columns = data.select_dtypes(include=['number']).columns
        if len(numeric_columns) > 0:
            st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
            st.markdown("#### Key Metrics")
            metrics = st.columns(len(numeric_columns))
            for i, col in enumerate(numeric_columns):
                metrics[i].metric(f"{col} Sum", f"{data[col].sum():,.2f}")
            st.markdown('</div>', unsafe_allow_html=True)

        # Visualization options
        st.subheader("📊 Create Visualizations")

        # Select columns for X and Y axes
        available_columns = data.columns.tolist()
        x_axis = st.selectbox("Select X-axis", available_columns)
        y_axis = st.selectbox("Select Y-axis", numeric_columns)

        # Select chart type
        chart_type = st.radio(
            "Select Chart Type",
            ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart"],
            horizontal=True,
        )

        # Generate chart
        if st.button("Generate Chart"):
            if chart_type == "Bar Chart":
                fig = px.bar(data, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
            elif chart_type == "Line Chart":
                fig = px.line(data, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
            elif chart_type == "Scatter Plot":
                fig = px.scatter(data, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
            elif chart_type == "Pie Chart" and x_axis:
                fig = px.pie(data, names=x_axis, values=y_axis, title=f"{y_axis} Distribution by {x_axis}")
            else:
                st.warning("Invalid chart configuration.")
                fig = None

            if fig:
                st.plotly_chart(fig, use_container_width=True)

# Additional Insights Section
if uploaded_file and not data.empty:
    st.subheader("📈 Additional Insights")
    st.write("You can extend this section with more visualizations or custom analytics based on your data.")
