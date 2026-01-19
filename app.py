import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
import random
import time
import re
from datetime import datetime
import textstat
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud

# Download nltk data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except:
    nltk.download('punkt')
    nltk.download('stopwords')

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SEO Blog Studio Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1a2980 0%, #26d0ce 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 10px;
        color: white;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .keyword-chip {
        display: inline-block;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 8px 16px;
        margin: 5px;
        border-radius: 25px;
        color: white;
        font-weight: 600;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    .section-card {
        background: rgba(30, 41, 59, 0.8);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        backdrop-filter: blur(10px);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 25px;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #00c9ff 0%, #92fe9d 100%);
        height: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h2>⚙️ Settings</h2>
        <hr style="border-color: #667eea;">
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎯 Blog Type")
    blog_type = st.selectbox(
        "Select Content Type",
        ["How-to Guide", "Listicle", "Case Study", "Ultimate Guide", "Comparison", "News Article"]
    )
    
    st.markdown("### 📊 Target Metrics")
    target_word_count = st.slider("Target Word Count", 500, 3000, 1200)
    target_keywords = st.number_input("Number of Keywords", 1, 20, 5)
    target_readability = st.slider("Target Readability Score", 0, 100, 70)
    
    st.markdown("### 🎨 Theme")
    theme_color = st.color_picker("Dashboard Theme", "#667eea")
    
    if st.button("🔄 Reset Dashboard"):
        st.rerun()

# ---------------- MAIN DASHBOARD ----------------
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown("""
    <div class="main-header">
        <h1>🚀 SEO Blog Research & Writing Studio</h1>
        <p>AI-Powered Content Research • Semantic Analysis • SEO Optimization</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>📅 Date</h3>
        <h2>{}</h2>
    </div>
    """.format(datetime.now().strftime("%d %b %Y")), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>⚡ Status</h3>
        <h2>🟢 Active</h2>
    </div>
    """, unsafe_allow_html=True)

# ---------------- KEYWORD RESEARCH SECTION ----------------
st.markdown("""
<div class="section-card">
    <h2>🔍 Keyword Research Center</h2>
    <p>Enter your primary keyword to get comprehensive SEO insights</p>
</div>
""", unsafe_allow_html=True)

primary_keyword = st.text_input("🎯 Enter Primary Keyword (e.g., 'digital marketing', 'Python tutorial', 'healthy recipes'):", 
                                placeholder="Type your main keyword here...")

# Sample keyword database (in real app, you'd use API)
KEYWORD_DATABASE = {
    "digital marketing": {
        "volume": 74000,
        "difficulty": 72,
        "cpc": 12.45,
        "trend": "increasing",
        "related": ["social media marketing", "content marketing", "seo", "email marketing", "ppc", "inbound marketing", "affiliate marketing"]
    },
    "python tutorial": {
        "volume": 135000,
        "difficulty": 45,
        "cpc": 1.23,
        "trend": "stable",
        "related": ["python for beginners", "django tutorial", "machine learning python", "data analysis python", "web scraping python"]
    },
    "healthy recipes": {
        "volume": 246000,
        "difficulty": 68,
        "cpc": 2.15,
        "trend": "increasing",
        "related": ["easy recipes", "keto recipes", "vegetarian recipes", "meal prep", "healthy breakfast", "low carb recipes"]
    }
}

if primary_keyword:
    # ---------------- KEYWORD METRICS ----------------
    st.markdown("### 📊 Keyword Analysis")
    
    # Get keyword data or generate mock data
    if primary_keyword.lower() in KEYWORD_DATABASE:
        keyword_data = KEYWORD_DATABASE[primary_keyword.lower()]
    else:
        # Generate mock data for new keywords
        keyword_data = {
            "volume": random.randint(10000, 250000),
            "difficulty": random.randint(30, 90),
            "cpc": round(random.uniform(0.5, 20.0), 2),
            "trend": random.choice(["increasing", "decreasing", "stable"]),
            "related": [
                f"{primary_keyword} for beginners",
                f"best {primary_keyword}",
                f"{primary_keyword} strategies",
                f"{primary_keyword} tips",
                f"advanced {primary_keyword}"
            ]
        }
    
    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4>📈 Search Volume</h4>
            <h2>{keyword_data['volume']:,}</h2>
            <p>Monthly searches</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>⚡ Difficulty</h4>
            <h2>{keyword_data['difficulty']}/100</h2>
            <div class="progress-bar" style="width: {keyword_data['difficulty']}%"></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h4>💰 CPC</h4>
            <h2>${keyword_data['cpc']}</h2>
            <p>Cost per click</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        trend_icon = "📈" if keyword_data['trend'] == 'increasing' else "📉" if keyword_data['trend'] == 'decreasing' else "➡️"
        st.markdown(f"""
        <div class="metric-card">
            <h4>📊 Trend</h4>
            <h2>{trend_icon} {keyword_data['trend'].title()}</h2>
            <p>Search trend</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ---------------- RELATED KEYWORDS ----------------
    st.markdown("### 🔗 Related Keywords & LSI Terms")
    
    related_keywords = keyword_data['related']
    
    # Display keyword chips
    keywords_html = "".join([f"<span class='keyword-chip'>{kw}</span>" for kw in related_keywords])
    st.markdown(f"""
    <div style='padding: 20px; background: rgba(30, 41, 59, 0.5); border-radius: 15px; margin: 20px 0;'>
        {keywords_html}
    </div>
    """, unsafe_allow_html=True)
    
    # ---------------- VISUALIZATIONS ----------------
    col1, col2 = st.columns(2)
    
    with col1:
        # Create word cloud
        st.markdown("### ☁️ Keyword Cloud")
        wordcloud_text = " ".join([primary_keyword] * 10 + related_keywords * 5)
        wordcloud = WordCloud(width=400, height=300, background_color='#0e1117', 
                             colormap='viridis').generate(wordcloud_text)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    
    with col2:
        # Create keyword metrics radar chart
        st.markdown("### 📊 Keyword Metrics Radar")
        
        categories = ['Volume', 'Difficulty', 'CPC', 'Competition', 'Opportunity']
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=[keyword_data['volume']/2500, keyword_data['difficulty'], 
               keyword_data['cpc']*5, random.randint(40, 90), random.randint(30, 85)],
            theta=categories,
            fill='toself',
            name=primary_keyword,
            line_color='#667eea'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # ---------------- CONTENT GENERATION ----------------
    st.markdown("""
    <div class="section-card">
        <h2>✍️ AI Content Generator</h2>
        <p>Generate SEO-optimized content based on your keyword research</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Blog title generator
    st.markdown("### 🎯 Blog Title Generator")
    
    # Generate title suggestions
    title_templates = [
        f"The Ultimate Guide to {primary_keyword.title()} in 2024",
        f"10 Proven {primary_keyword.title()} Strategies That Actually Work",
        f"How to Master {primary_keyword.title()}: A Beginner's Guide",
        f"The Future of {primary_keyword.title()}: Trends and Predictions",
        f"{primary_keyword.title()} Explained: Everything You Need to Know"
    ]
    
    selected_title = st.selectbox("Choose or edit your blog title:", title_templates)
    custom_title = st.text_input("Or write your own title:", value=selected_title)
    
    # Content generation
    if st.button("🚀 Generate SEO-Optimized Content", use_container_width=True):
        with st.spinner("✨ Generating amazing content for you..."):
            progress_bar = st.progress(0)
            
            for i in range(100):
                time.sleep(0.02)
                progress_bar.progress(i + 1)
            
            # Generate sample content structure
            sections = [
                f"## Introduction to {primary_keyword}",
                f"### Why {primary_keyword} Matters Today",
                f"### Key Benefits of Effective {primary_keyword}",
                "## Getting Started",
                "### Essential Tools and Resources",
                "### Common Mistakes to Avoid",
                f"## Advanced {primary_keyword} Strategies",
                "## Case Studies and Examples",
                "## Future Trends and Predictions",
                "## Conclusion and Next Steps"
            ]
            
            # Generate content for each section
            generated_content = f"# {custom_title}\n\n"
            
            for section in sections:
                generated_content += f"{section}\n\n"
                # Add sample content
                sentences = [
                    f"This section explores the important aspects of {primary_keyword.lower()} and how it impacts modern strategies.",
                    f"Understanding these concepts will help you implement more effective {primary_keyword.lower()} techniques.",
                    "Research shows that businesses adopting these methods see significant improvements in their results.",
                    f"Let's dive deeper into the practical applications of {primary_keyword.lower()} with real-world examples.",
                    "These insights are based on current industry trends and successful case studies."
                ]
                paragraph = " ".join(random.sample(sentences, 3))
                generated_content += f"{paragraph}\n\n"
                
                # Add bullet points randomly
                if random.random() > 0.5:
                    generated_content += "**Key Takeaways:**\n\n"
                    bullet_points = [
                        f"Important aspect of {primary_keyword.lower()}",
                        "Practical implementation tips",
                        "Industry best practices",
                        "Common pitfalls to avoid",
                        "Tools and resources"
                    ]
                    for point in random.sample(bullet_points, 3):
                        generated_content += f"- {point}\n"
                    generated_content += "\n"
            
            # Display generated content
            st.markdown("### 📄 Generated Content Preview")
            st.text_area("Edit your content:", generated_content, height=400)
            
            # ---------------- SEO ANALYSIS ----------------
            st.markdown("### 📊 SEO Analysis")
            
            # Calculate metrics
            word_count = len(generated_content.split())
            sentence_count = len(re.split(r'[.!?]+', generated_content))
            paragraph_count = len(generated_content.split('\n\n'))
            
            # Readability score
            readability = textstat.flesch_reading_ease(generated_content)
            seo_score = min(100, max(0, readability))
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>📝 Word Count</h4>
                    <h2>{word_count}</h2>
                    <p>Target: {target_word_count}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>📚 Readability</h4>
                    <h2>{int(seo_score)}/100</h2>
                    <div class="progress-bar" style="width: {seo_score}%"></div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>📖 Sentences</h4>
                    <h2>{sentence_count}</h2>
                    <p>Average length: {word_count//sentence_count if sentence_count > 0 else 0}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>📑 Paragraphs</h4>
                    <h2>{paragraph_count}</h2>
                    <p>Content structure</p>
                </div>
                """, unsafe_allow_html=True)
            
            # ---------------- KEYWORD DENSITY ANALYSIS ----------------
            st.markdown("### 🔍 Keyword Density Analysis")
            
            # Simple keyword density calculation
            content_words = re.findall(r'\b\w+\b', generated_content.lower())
            word_freq = Counter(content_words)
            top_keywords = word_freq.most_common(10)
            
            # Create keyword density dataframe
            density_df = pd.DataFrame(top_keywords, columns=['Keyword', 'Frequency'])
            density_df['Density (%)'] = (density_df['Frequency'] / len(content_words) * 100).round(2)
            
            # Display as bar chart
            fig = px.bar(density_df.head(8), x='Keyword', y='Density (%)',
                        color='Density (%)',
                        color_continuous_scale='viridis',
                        title='Top Keyword Density')
            fig.update_layout(template='plotly_dark',
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            
            # ---------------- DOWNLOAD OPTIONS ----------------
            st.markdown("### 💾 Export Your Content")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📄 Download as TXT", use_container_width=True):
                    st.download_button(
                        label="Click to Download",
                        data=generated_content,
                        file_name=f"{primary_keyword.lower().replace(' ', '_')}_blog.txt",
                        mime="text/plain"
                    )
            
            with col2:
                if st.button("📝 Download as DOCX", use_container_width=True):
                    # Create a simple text file for download
                    st.download_button(
                        label="Click to Download",
                        data=generated_content,
                        file_name=f"{primary_keyword.lower().replace(' ', '_')}_blog.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
            
            with col3:
                if st.button("📊 Download Report", use_container_width=True):
                    # Create a simple report
                    report = f"""
                    SEO CONTENT REPORT
                    ==================
                    
                    Keyword: {primary_keyword}
                    Title: {custom_title}
                    Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                    
                    METRICS:
                    - Word Count: {word_count}
                    - Readability Score: {int(seo_score)}/100
                    - Sentences: {sentence_count}
                    - Paragraphs: {paragraph_count}
                    
                    TOP KEYWORDS:
                    """
                    for kw, freq in top_keywords[:5]:
                        report += f"\n- {kw}: {freq} times"
                    
                    st.download_button(
                        label="Click to Download",
                        data=report,
                        file_name=f"{primary_keyword.lower().replace(' ', '_')}_report.txt",
                        mime="text/plain"
                    )
            
            st.success("✅ Content generated successfully! You can now edit, analyze, and download your SEO-optimized blog post.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; padding: 2rem;">
    <p>🚀 <strong>SEO Blog Studio Pro</strong> • AI-Powered Content Creation • v2.0</p>
    <p style="font-size: 0.9rem;">Generate SEO-optimized content without uploading files | Real-time analysis | Export multiple formats</p>
</div>
""", unsafe_allow_html=True)
# Note: This is a simplified example. In a production app, you would integrate with real SEO APIs and AI content generation services.