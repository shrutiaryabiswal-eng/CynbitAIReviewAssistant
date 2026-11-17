
import streamlit as st
import pandas as pd
import plotly.express as px

from src.sentiment import SentimentAnalyzer
from src.classification import classify_issue
from src.priority import detect_priority
from src.response_generator import generate_response
from src.database import (
    initialize_database,
    save_analysis,
    get_history
)


# --------------------------------------------------
# 1. PAGE CONFIGURATION AND DATABASE INITIALIZATION
# --------------------------------------------------

st.set_page_config(
    page_title="Revio InsightAI",
    page_icon="🤖",
    layout="wide"
)

initialize_database()

st.title("🤖 Revio InsightAI")

st.caption(
    "Explainable AI-powered customer review intelligence"
)


# --------------------------------------------------
# 2. LOAD MACHINE LEARNING MODEL
# --------------------------------------------------

@st.cache_resource
def load_model():

    data = pd.read_csv("data/sample_reviews.csv")

    analyzer = SentimentAnalyzer()

    analyzer.train(
        data["review"].tolist(),
        data["rating"].tolist()
    )

    return analyzer


try:
    analyzer = load_model()

except Exception as error:

    st.error(f"Could not load the ML model: {error}")
    st.stop()


# --------------------------------------------------
# 3. REVIEW ANALYSIS FUNCTION
# --------------------------------------------------

def analyze_review(review, rating):

    sentiment_result = analyzer.predict(review)

    sentiment = sentiment_result["sentiment"]

    category = classify_issue(review)

    priority_result = detect_priority(
        review,
        sentiment,
        rating
    )

    response = generate_response(
        review,
        sentiment,
        category
    )

    return {
        "Review": review,
        "Rating": rating,
        "Sentiment": sentiment,
        "Confidence": sentiment_result["confidence"],
        "Category": category,
        "Priority": priority_result["priority"],
        "Reason": ", ".join(priority_result["reasons"])
            or "No immediate risk detected",
        "Suggested Response": response
    }


# --------------------------------------------------
# 4. SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("Revio InsightAI")

st.sidebar.caption("Customer Review Intelligence")

page = st.sidebar.radio(
    "Choose a page",
    [
        "Dashboard",
        "Analyze Review",
        "Upload Reviews",
        "Review History"
    ]
)


# --------------------------------------------------
# 5. DASHBOARD PAGE
# --------------------------------------------------

if page == "Dashboard":

    st.subheader("📊 Review Intelligence Dashboard")

    data = pd.read_csv("data/sample_reviews.csv")

    results = [
        analyze_review(row["review"], row["rating"])
        for _, row in data.iterrows()
    ]

    results_df = pd.DataFrame(results)

    # --------------------------------------------------
    # SENTIMENT MODEL EVALUATION
    # --------------------------------------------------

    st.divider()
    st.subheader("🧠 Sentiment Model Evaluation")

    evaluation = analyzer.evaluate(
        data["review"].tolist(),
        data["rating"].tolist()
    )

    eval_col1, eval_col2 = st.columns(2)

    eval_col1.metric(
        "Test Accuracy",
        f"{evaluation['accuracy']:.1%}"
    )

    eval_col2.metric(
        "Test Samples",
        evaluation["test_samples"]
    )

    st.caption(
        "Evaluation uses a stratified held-out test set. "
        "Sentiment labels are derived from customer ratings."
    )

    # Display precision, recall and F1-score
    report = evaluation["classification_report"]

    report_df = pd.DataFrame([
        {
            "Sentiment": sentiment.title(),
            "Precision": report[sentiment]["precision"],
            "Recall": report[sentiment]["recall"],
            "F1-score": report[sentiment]["f1-score"],
            "Support": int(report[sentiment]["support"])
        }
        for sentiment in ["negative", "neutral", "positive"]
    ])

    st.write("#### Classification Performance")

    st.dataframe(
        report_df,
        use_container_width=True,
        hide_index=True
    )

    # Display confusion matrix
    st.write("#### Confusion Matrix")

    labels = ["Negative", "Neutral", "Positive"]

    confusion_df = pd.DataFrame(
        evaluation["confusion_matrix"],
        index=labels,
        columns=labels
    )

    fig = px.imshow(
        confusion_df,
        text_auto=True,
        labels={
            "x": "Predicted Sentiment",
            "y": "Actual Sentiment",
            "color": "Number of Reviews"
        },
        title="Actual vs Predicted Sentiment",
        color_continuous_scale="Blues"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        "This is a prototype evaluation using synthetic data. "
        "Results should not be interpreted as real-world "
        "customer sentiment accuracy."
    )

    st.divider()


    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Reviews",
        len(results_df)
    )

    col2.metric(
        "Negative Reviews",
        int((results_df["Sentiment"] == "negative").sum())
    )

    col3.metric(
        "High Priority",
        int((results_df["Priority"] == "High").sum())
    )

    col4.metric(
        "Average Rating",
        round(results_df["Rating"].mean(), 2)
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        sentiment_counts = (
            results_df["Sentiment"]
            .value_counts()
            .reset_index()
        )

        sentiment_counts.columns = [
            "Sentiment",
            "Count"
        ]

        fig = px.pie(
            sentiment_counts,
            names="Sentiment",
            values="Count",
            title="Sentiment Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        category_counts = (
            results_df["Category"]
            .value_counts()
            .reset_index()
        )

        category_counts.columns = [
            "Category",
            "Count"
        ]

        fig = px.bar(
            category_counts,
            x="Category",
            y="Count",
            title="Customer Complaint Categories"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Review Analysis")

    st.dataframe(
        results_df,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# 6. ANALYZE INDIVIDUAL REVIEW PAGE
# --------------------------------------------------

elif page == "Analyze Review":

    st.subheader("🔍 Analyze an Individual Review")

    review = st.text_area(
        "Enter customer review",
        placeholder="Example: My refund has not arrived..."
    )

    rating = st.slider(
        "Customer Rating",
        min_value=1,
        max_value=5,
        value=2
    )

    if st.button("Analyze Review", type="primary"):

        if not review.strip():

            st.warning("Please enter a customer review.")

        else:

            result = analyze_review(review, rating)

            save_analysis(result)

            st.success(
                "Analysis completed and saved successfully!"
            )

            st.subheader("Analysis Results")

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Sentiment",
                result["Sentiment"]
            )

            c2.metric(
                "Issue Category",
                result["Category"]
            )

            c3.metric(
                "Priority",
                result["Priority"]
            )

            st.write(
                "Model confidence:",
                f"{result['Confidence']:.1%}"
            )

            st.write("### Why was this flagged?")

            st.info(result["Reason"])

            st.write("### Suggested Customer Response")

            st.success(result["Suggested Response"])

            st.caption(
                "This response is a draft. A human must review "
                "and approve it before sending."
            )


# --------------------------------------------------
# 7. UPLOAD CUSTOMER REVIEWS PAGE
# --------------------------------------------------

elif page == "Upload Reviews":

    st.subheader("📁 Upload Customer Reviews")

    uploaded_file = st.file_uploader(
        "Upload a CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:

            uploaded_data = pd.read_csv(uploaded_file)

            if not {"review", "rating"}.issubset(
                uploaded_data.columns
            ):

                st.error(
                    "CSV must contain 'review' and 'rating' columns."
                )

            else:

                results = []

                for _, row in uploaded_data.iterrows():

                    review_text = str(row["review"])

                    rating_value = int(row["rating"])

                    if not 1 <= rating_value <= 5:
                        raise ValueError(
                            "Ratings must be between 1 and 5."
                        )

                    result = analyze_review(
                        review_text,
                        rating_value
                    )

                    results.append(result)

                    save_analysis(result)

                results_df = pd.DataFrame(results)

                st.success(
                    "Reviews analyzed and saved successfully!"
                )

                st.dataframe(
                    results_df,
                    use_container_width=True,
                    hide_index=True
                )

                csv = results_df.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    "Download Analysis Report",
                    data=csv,
                    file_name="review_analysis.csv",
                    mime="text/csv"
                )

        except Exception as error:

            st.error(f"Could not process uploaded file: {error}")


# --------------------------------------------------
# 8. REVIEW HISTORY PAGE
# --------------------------------------------------

elif page == "Review History":

    st.subheader("🗂️ Saved Review History")

    history = get_history()

    if history:

        columns = [
            "ID",
            "Review",
            "Rating",
            "Sentiment",
            "Confidence",
            "Category",
            "Priority",
            "Reason",
            "Suggested Response",
            "Created At"
        ]

        history_df = pd.DataFrame(
            history,
            columns=columns
        )

        st.metric(
            "Total Saved Reviews",
            len(history_df)
        )

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

        csv = history_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "Download Review History",
            data=csv,
            file_name="review_history.csv",
            mime="text/csv"
        )

    else:

        st.info(
            "No saved reviews yet. Analyze a review first."
        )


# --------------------------------------------------
# 9. FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Revio InsightAI | AI-powered Review Intelligence "
    "| Human-in-the-loop decision support"
)
