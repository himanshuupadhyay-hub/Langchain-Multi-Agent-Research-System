import streamlit as st
from src.pipelines.pipelines import research_pipeline 

st.set_page_config(page_title="AI Research Agent", layout="wide")

st.title("🔎 AI Research Assistant")
st.write("Enter a topic and let the agents search, scrape, write, and critique a report for you.")

topic = st.text_input("Enter a topic to research:", placeholder="e.g. Latest advancements in RAG pipelines")

run_button = st.button("Run Research Pipeline", type="primary")

if run_button:
    if not topic.strip():
        st.warning("Please enter a topic before running the pipeline.")
    else:
        with st.spinner("Running the agents... this may take a moment."):
            try:
                result = research_pipeline(topic)
            except Exception as e:
                st.error(f"Pipeline failed: {e}")
                st.stop()

        st.success("Pipeline completed!")

        # Tabs to show each stage's output
        tab1, tab2, tab3, tab4 = st.tabs(["🔍 Search Results", "📄 Scraped Content", "📝 Final Report", "🧐 Critic Feedback"])

        with tab1:
            st.subheader("Search Agent Output")
            st.write(result.get("search_results", "No search results found."))

        with tab2:
            st.subheader("Reader Agent Output")
            st.write(result.get("scraped_content", "No scraped content found."))

        with tab3:
            st.subheader("Final Report")
            st.write(result.get("report", "No report generated."))

        with tab4:
            st.subheader("Critic's Feedback")
            st.write(result.get("feedback", "No feedback generated."))

        # Optional: download the final report
        if result.get("report"):
            st.download_button(
                label="Download Report as .txt",
                data=str(result["report"]),
                file_name=f"{topic.replace(' ', '_')}_report.txt",
                mime="text/plain"
            )
