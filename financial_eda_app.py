import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from sklearn.preprocessing import StandardScaler

# ----------------------
# DATA LOADING FUNCTION
# ----------------------
def load_dataset(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        return pd.read_excel(file)
    else:
        raise ValueError("Unsupported file format")

# ----------------------
# DATA PREPROCESSING
# ----------------------
def preprocess_data(df):
    df = df.drop_duplicates()

    # Convert object columns to numeric where possible
    for col in df.select_dtypes(include='object').columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df.fillna(df.mean(numeric_only=True), inplace=True)
    df = df.convert_dtypes()
    return df

# ----------------------
# EDA FUNCTIONS
# ----------------------
def describe_data(df):
    return df.describe()

def correlation_matrix(df):
    return df.corr()

def standardize_data(df, columns):
    scaler = StandardScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df

def identify_outliers(df, column):
    df = df.copy()
    df[column] = pd.to_numeric(df[column], errors='coerce')
    df = df.dropna(subset=[column])

    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return df[(df[column] < lower) | (df[column] > upper)]

# ----------------------
# VISUALIZATION FUNCTIONS
# ----------------------
def plot_histogram(df, column):
    df = df.copy()
    df[column] = pd.to_numeric(df[column], errors='coerce')
    df = df.dropna(subset=[column])

    if df[column].empty:
        st.warning(f"No valid numeric data found in '{column}' for histogram.")
        return

    fig, ax = plt.subplots()
    try:
        sns.histplot(df[column], kde=False, ax=ax)  # kde=False to prevent KDE errors
        ax.set_title(f"Histogram of {column}")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error in plotting histogram: {e}")

def plot_boxplot(df, column):
    df = df.copy()
    df[column] = pd.to_numeric(df[column], errors='coerce')
    df = df.dropna(subset=[column])

    if not pd.api.types.is_numeric_dtype(df[column]):
        st.warning(f"{column} is not numeric. Skipping boxplot.")
        return

    fig, ax = plt.subplots()
    sns.boxplot(x=df[column], ax=ax)
    ax.set_title(f"Boxplot of {column}")
    st.pyplot(fig)

def interactive_line_plot(df, x, y):
    df = df.copy()
    df[y] = pd.to_numeric(df[y], errors='coerce')
    df = df.dropna(subset=[x, y])

    if not pd.api.types.is_numeric_dtype(df[y]):
        st.warning(f"{y} is not numeric. Cannot plot line chart.")
        return

    fig = px.line(df, x=x, y=y, title=f"{y} over {x}")
    st.plotly_chart(fig)

# ----------------------
# STREAMLIT APP
# ----------------------
def run_streamlit_app():
    st.set_page_config(page_title="Financial EDA Tool", layout="wide")
    st.title("📊 Exploratory Data Analysis Tool for Financial Data")

    uploaded_file = st.file_uploader("Upload a financial dataset (.csv or .xlsx)", type=["csv", "xlsx"])
    if uploaded_file:
        df = load_dataset(uploaded_file)
        st.success("File uploaded successfully.")
        st.subheader("Data Preview")
        st.dataframe(df.head())

        df = preprocess_data(df)

        if st.checkbox("Show Descriptive Statistics"):
            st.subheader("Descriptive Statistics")
            st.write(describe_data(df))

        if st.checkbox("Show Correlation Matrix with Heatmap"):
            st.subheader("Correlation Matrix")
            corr = correlation_matrix(df)
            st.dataframe(corr)
            fig, ax = plt.subplots()
            sns.heatmap(corr, annot=True, cmap="YlGnBu", ax=ax)
            st.pyplot(fig)

        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if numeric_cols:
            selected_col = st.selectbox("Select column for Histogram/Boxplot", numeric_cols)
            plot_histogram(df, selected_col)
            plot_boxplot(df, selected_col)

            if st.checkbox("Show Outliers"):
                outliers = identify_outliers(df, selected_col)
                st.write(f"Outliers in {selected_col}:", outliers)

            if st.checkbox("Interactive Line Plot"):
                x_axis = st.selectbox("Select X-axis", df.columns)
                y_axis = st.selectbox("Select Y-axis", numeric_cols)
                interactive_line_plot(df, x_axis, y_axis)

# Run the Streamlit app
run_streamlit_app()
