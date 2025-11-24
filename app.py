# =============================================
# World Happiness Dashboard (2015-2019)
# =============================================
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1 Load dataset
df = pd.read_csv(r'D:\a_CFP_Farhana\mentor_ssions\Dataset\happiness report\happiness_combined_cleann.csv')

st.set_page_config(layout="wide")
st.title(" World Happiness Dashboard (2015-2019)")
st.markdown("> Explore factors influencing happiness across countries and years.")

# =============================================
# 2 Static KPIs
# =============================================
st.markdown("### 🎯 Global Happiness Highlights")


col1, col2, col3 = st.columns(3)
col1.metric("😊 Score", f"{df['Happiness_Score'].mean():.2f}")
col2.metric("📍 Rank", f"{df['Happiness_Rank'].mean():.0f}")
col3.metric("💰 GDP", f"{df['GDP'].mean():.2f}")

col4, col5, col6 = st.columns(3)
col4.metric("❤️ Health", f"{df['Health'].mean():.2f}")
col5.metric("👪 Support", f"{df['Family'].mean():.2f}")
col6.metric("🕊️ Freedom", f"{df['Freedom'].mean():.2f}")

st.markdown("---")

# =============================================
# 3 Sidebar Filters 
# =============================================
st.sidebar.header("Filters & Options")
years = sorted(df['Year'].unique())
selected_year = st.sidebar.slider("Select Year", min_value=int(min(years)), max_value=int(max(years)), value=int(max(years)))

top_n = st.sidebar.number_input("Top N Countries", min_value=1, max_value=20, value=10)
selected_factor = st.sidebar.selectbox("Select Factor for Scatter / Ranking", ['GDP','Health','Family','Freedom','Generosity','Trust'])
selected_country = st.sidebar.selectbox("Select Country for Trend", df['Country'].unique())
multi_countries = st.sidebar.multiselect("Compare Multiple Countries", df['Country'].unique(), default=["Finland","United States"])

# Filter dataset by year
year_df = df[df['Year'] == selected_year]

# =============================================
# 4 Top / Bottom Countries Bar Chart
# =============================================
st.subheader(f"Top {top_n} Happiest Countries in {selected_year}")
top_countries = year_df.sort_values('Happiness_Score', ascending=False).head(top_n)
fig_top = px.bar(top_countries, x='Happiness_Score', y='Country', orientation='h', color='Happiness_Score', text='Happiness_Score', color_continuous_scale='Viridis')
st.plotly_chart(fig_top, use_container_width=True)

st.subheader(f"Bottom {top_n} Countries in {selected_year}")
bottom_countries = year_df.sort_values('Happiness_Score').head(top_n)
fig_bottom = px.bar(bottom_countries, x='Happiness_Score', y='Country', orientation='h', color='Happiness_Score', text='Happiness_Score', color_continuous_scale='Magma')
st.plotly_chart(fig_bottom, use_container_width=True)
st.markdown("---")
# =============================================
# 5 Scatter Plot: Happiness vs Selected Factor
# =============================================
st.subheader(f"Happiness Score vs {selected_factor} ({selected_year})")
fig_scatter = px.scatter(year_df, x=selected_factor, y='Happiness_Score', text='Country', trendline="ols",
                         color='Happiness_Score', color_continuous_scale='Viridis', size='GDP')
st.plotly_chart(fig_scatter, use_container_width=True)
st.markdown("---")
# =============================================
# 6 Trend of Selected Country
# =============================================
st.subheader(f"Happiness Score Trend: {selected_country} (2015-2019)")
country_df = df[df['Country'] == selected_country]
fig_trend = px.line(country_df, x='Year', y='Happiness_Score', markers=True, title=f'{selected_country} Happiness Trend')
st.plotly_chart(fig_trend, use_container_width=True)
st.markdown("---")
# =============================================
# 7 Multi-Country Trend Comparison
# =============================================
if multi_countries:
    st.subheader("Happiness Score Trend Comparison")
    compare_df = df[df['Country'].isin(multi_countries)]
    fig_compare = px.line(compare_df, x='Year', y='Happiness_Score', color='Country', markers=True,
                          title='Happiness Trends of Selected Countries')
    st.plotly_chart(fig_compare, use_container_width=True)
st.markdown("---")
# =============================================
# 8 Correlation Heatmap for Selected Year
# =============================================
st.subheader(f"Correlation Heatmap ({selected_year})")
numeric_cols = ['GDP','Family','Health','Freedom','Generosity','Trust','Happiness_Score']
corr_df = year_df[numeric_cols].corr()
fig_corr = px.imshow(corr_df, text_auto=True, color_continuous_scale='RdBu_r', origin='lower')
st.plotly_chart(fig_corr, use_container_width=True)
st.markdown("---")
# =============================================
# 9 Factor Distribution Histogram
# =============================================
# selected_factor could be GDP, Health, Family, Freedom, Generosity, or Trust.
# The histogram splits all countries into bins based on the value of that factor.
# The height of each bin shows how many countries fall into that range.

st.subheader(f"Distribution of {selected_factor} ({selected_year})")
fig_hist = px.histogram(year_df, x=selected_factor, nbins=20, marginal="box", color_discrete_sequence=['teal'])
st.plotly_chart(fig_hist, use_container_width=True)
st.markdown("---")
# =============================================
# 10 Factor Ranking Table
# =============================================
st.subheader(f"Top {top_n} Countries by {selected_factor} ({selected_year})")
factor_top = year_df.sort_values(selected_factor, ascending=False).head(top_n)
st.dataframe(factor_top[['Country', selected_factor, 'Happiness_Score']])
st.markdown("---")