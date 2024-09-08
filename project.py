import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Main Function
def main():
    st.title("CSV Table Visualizer and Statistics")

    # Function to display the current dataset
    def show_dataset(df):
        st.write(" Updated Dataset Preview")
        st.write(df.head())
        st.write(f"Dataset size: {df.shape}")


    # Upload CSV
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        # Read CSV into DataFrame
        df = pd.read_csv(uploaded_file)
        st.write("### Dataset Preview")
        st.write(df)  # Display first few rows
        st.write(f"Dataset size: {df.shape}")
   
        st.write("### Dataset Analysis")
        # Toggle for showing statistics options
        show_statistics = st.checkbox("Show Analysis Options")
        
        if show_statistics:
            # Display basic statistics
            if st.checkbox("Show Basic Statistics"):
                st.write(df.describe())  # Describe gives summary statistics for numerical data
                st.write("Count of NaN (missing) Values")
                nan_count = df.isna().sum()  # Count NaN values per column
                st.write(nan_count)

            # Data Filtering
            if st.checkbox("Filter Data"):
                column = st.selectbox("Choose a column to filter", df.columns)
                unique_values = df[column].unique()
                selected_value = st.selectbox("Choose a value", unique_values)
                filtered_df = df[df[column] == selected_value]
                st.write(f"### Filtered Data by {column} = {selected_value}")
                st.write(filtered_df)
            
            # Correlation Heatmap with automatic exclusion of non-numeric columns
            if st.checkbox("Show Correlation Heatmap"):
                # Select only numeric columns
                numeric_df = df.select_dtypes(include=['int', 'float'])
                
                if numeric_df.empty:
                    st.write("No numeric columns available for correlation.")
                else:
                    st.write("### Correlation Heatmap (Numeric Columns Only)")
                    corr = numeric_df.corr()  # Calculate correlation matrix on numeric data
                    plt.figure(figsize=(10, 6))
                    sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
                    st.pyplot(plt)

        st.write("### Dataset Proccessing")
        # Toggle for showing processing options
        show_processing = st.checkbox("Show Processing Options")
        
        if show_processing:
            new_df = df.copy()
            # Handling Missing Data
            if st.checkbox("Handle Missing Data"):
                method = st.selectbox("Choose how to handle missing data", ["Fill with Mean", "Fill with Median", "Drop Rows with NaNs", "Drop Columns with NaNs"])
                if method == "Fill with Mean":
                    new_df.fillna(df.mean(), inplace=True)
                    st.write("Filled missing values with mean.")
                elif method == "Fill with Median":
                    new_df.fillna(df.median(), inplace=True)
                    st.write("Filled missing values with median.")
                elif method == "Drop Rows with NaNs":
                    new_df.dropna(axis=0, inplace=True)
                    st.write("Dropped rows with NaN values.")
                elif method == "Drop Columns with NaNs":
                    new_df.dropna(axis=1, inplace=True)
                    st.write("Dropped columns with NaN values.")
                st.write(new_df.head(10))  # Show updated data
                st.write(f"New Dataset size: {new_df.shape}")
                st.write(f"Old Dataset size: {df.shape}")
                

            # Data Normalization
            if st.checkbox("Normalize Data"):
                column_to_normalize = st.selectbox("Choose a column to normalize", new_df.select_dtypes(include=['int', 'float']).columns)
                new_df[column_to_normalize] = (new_df[column_to_normalize] - new_df[column_to_normalize].min()) / (new_df[column_to_normalize].max() - new_df[column_to_normalize].min())
                st.write(f"Normalized data in column: {column_to_normalize}")
                st.write(new_df.head(10))

            # Removing Duplicates
            if st.checkbox("Remove Duplicate Rows"):
                new_df = new_df.drop_duplicates()
                st.write("Duplicate rows removed.")
                st.write(new_df.head(10))
                st.write(f"New Dataset size: {new_df.shape}")
                st.write(f"Old Dataset size: {df.shape}")

        
            # Apply changes
            st.write('\n Apply changes/Download Dataset')
            if st.button("Apply chagnes"):
                try: df = new_df.copy()
                except: st.write('The changes could not be applied')
                else:
                    del new_df
                    st.write('The changes have been applied')
                    show_dataset(df)
        
            # Save (Download) New Dataset Functionality
            if st.button("Download Processed Dataset"):
                st.write("Download the Processed Dataset")

                # Convert DataFrame to CSV
                processed_csv = df.to_csv(index=False)

                # Provide download button
                st.download_button(
                    label="Download CSV",
                    data=processed_csv,
                    file_name="processed_dataset.csv",
                    mime="text/csv"
                )


        st.write("### Visualization Options")
        # Toggle for showing processing options
        show_vis = st.checkbox("Show Visualization Options")
        # Visualization Options
        if show_vis:
            chart_type = st.selectbox("Choose chart type", ["Histogram", "Scatter Plot", "Bar Chart", "Line Plot"])

            # Select columns for visualization
            if chart_type == "Histogram":
                column = st.selectbox("Choose column for histogram", df.select_dtypes(include=['int', 'float']).columns)
                plt.figure()
                sns.histplot(df[column], bins=30)
                st.pyplot(plt)

            elif chart_type == "Scatter Plot":
                x_column = st.selectbox("X-axis column", df.columns)
                y_column = st.selectbox("Y-axis column", df.columns)
                plt.figure()
                sns.scatterplot(x=x_column, y=y_column, data=df)
                st.pyplot(plt)

            elif chart_type == "Bar Chart":
                x_column = st.selectbox("X-axis column", df.columns)
                y_column = st.selectbox("Y-axis column", df.select_dtypes(include=['int', 'float']).columns)
                plt.figure()
                sns.barplot(x=x_column, y=y_column, data=df)
                st.pyplot(plt)

            elif chart_type == "Line Plot":
                x_column = st.selectbox("X-axis column", df.columns)
                y_column = st.selectbox("Y-axis column", df.select_dtypes(include=['int', 'float']).columns)
                plt.figure()
                sns.lineplot(x=x_column, y=y_column, data=df)
                st.pyplot(plt)
        
        


# Run the app
if __name__ == "__main__":
    main()
