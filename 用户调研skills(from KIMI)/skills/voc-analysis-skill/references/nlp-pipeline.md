# VOC NLP Pipeline — Python Implementation

Complete Python pipeline for processing user feedback data. Run in IPython environment.

## Full Pipeline

```python
import pandas as pd
import jieba
import numpy as np
from collections import Counter, defaultdict
from gensim import corpora, models
import re

# ============ 1. DATA LOADING ============
def load_feedback(file_path):
    """Load feedback from CSV/JSON. Expected columns: id, text, source, date, rating(optional)"""
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.json'):
        return pd.read_json(file_path)
    else:
        raise ValueError("Unsupported file format")

# ============ 2. PREPROCESSING ============
def clean_text(text):
    """Clean text: remove URLs, emails, HTML, special chars"""
    if pd.isna(text):
        return ""
    text = str(text)
    text = re.sub(r'http[s]?://\S+', '', text)  # URLs
    text = re.sub(r'\S+@\S+', '', text)          # Emails
    text = re.sub(r'<[^>]+>', '', text)           # HTML tags
    text = re.sub(r'[^\w\s\u4e00-\u9fff.,!?;:\-\'"()]', ' ', text)  # Keep Chinese + basic punct
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize_chinese(text, custom_dict=None):
    """Tokenize Chinese text with Jieba"""
    if custom_dict:
        for word in custom_dict:
            jieba.add_word(word)
    return list(jieba.cut(text))

STOPWORDS = set(['的', '了', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '可以', '吗', '吧', '啊', '呢', '哦', '嗯', '这个', '那个'])

def remove_stopwords(tokens):
    """Remove stopwords and short tokens"""
    return [t for t in tokens if t not in STOPWORDS and len(t) > 1]

# ============ 3. SENTIMENT ANALYSIS ============
def analyze_sentiment_basic(text):
    """Rule-based sentiment for Chinese"""
    positive_words = set(['好', '棒', '优秀', '喜欢', '爱', '满意', '推荐', '不错', '完美', '方便', '快', '清晰', '好用', '喜欢', '值得', '惊喜'])
    negative_words = set(['差', '烂', '糟糕', '失望', '垃圾', '慢', '卡', '崩溃', 'Bug', 'bug', '问题', '难用', '麻烦', '差劲', '后悔', '吐槽'])
    
    pos_count = sum(1 for w in positive_words if w in text)
    neg_count = sum(1 for w in negative_words if w in text)
    
    if pos_count > neg_count:
        return 'positive', min(5, 3 + pos_count - neg_count)
    elif neg_count > pos_count:
        return 'negative', max(1, 3 - neg_count + pos_count)
    else:
        return 'neutral', 3

# ============ 4. TOPIC MODELING (LDA) ============
def run_topic_modeling(tokenized_texts, num_topics=8):
    """Run LDA topic modeling"""
    dictionary = corpora.Dictionary(tokenized_texts)
    dictionary.filter_extremes(no_below=3, no_above=0.7)  # Filter rare/common words
    corpus = [dictionary.doc2bow(text) for text in tokenized_texts]
    
    lda_model = models.LdaModel(
        corpus=corpus, id2word=dictionary, num_topics=num_topics,
        random_state=42, passes=10, alpha='auto'
    )
    
    topics = []
    for idx, topic in lda_model.print_topics(num_words=8):
        topics.append({
            'id': idx,
            'keywords': [word.split('"')[1] for word in topic.split('+')],
            'weight': sum([float(w.split('*')[0]) for w in topic.split('+')])
        })
    return topics, lda_model, corpus, dictionary

# ============ 5. KEYWORD EXTRACTION ============
def extract_keywords(tokenized_texts, top_n=50):
    """Extract top keywords by frequency (excluding stopwords)"""
    all_tokens = [t for tokens in tokenized_texts for t in tokens]
    return Counter(all_tokens).most_common(top_n)

# ============ 6. FULL PIPELINE ============
def run_voc_analysis(file_path, custom_dict=None, num_topics=8):
    """Run complete VOC analysis pipeline"""
    # Load
    df = load_feedback(file_path)
    print(f"Loaded {len(df)} feedback items")
    
    # Preprocess
    df['clean_text'] = df['text'].apply(clean_text)
    df['tokens'] = df['clean_text'].apply(lambda x: tokenize_chinese(x, custom_dict))
    df['tokens'] = df['tokens'].apply(remove_stopwords)
    
    # Sentiment
    sentiments = df['clean_text'].apply(analyze_sentiment_basic)
    df['sentiment'] = sentiments.apply(lambda x: x[0])
    df['sentiment_score'] = sentiments.apply(lambda x: x[1])
    
    # Topic modeling
    tokenized = df['tokens'].tolist()
    topics, lda_model, corpus, dictionary = run_topic_modeling(tokenized, num_topics)
    
    # Keywords
    keywords = extract_keywords(tokenized)
    
    # Summary
    summary = {
        'total': len(df),
        'sentiment_dist': df['sentiment'].value_counts().to_dict(),
        'avg_sentiment': df['sentiment_score'].mean(),
        'topics': topics,
        'top_keywords': keywords[:20]
    }
    
    return df, summary, lda_model
```

## Usage Example

```python
# Run pipeline
df, summary, model = run_voc_analysis(
    file_path='feedback.csv',
    custom_dict=['产品名称', '功能A', '功能B'],  # Add product-specific terms
    num_topics=8
)

# View summary
print(f"Sentiment: {summary['sentiment_dist']}")
print(f"Top keywords: {summary['top_keywords'][:10]}")
for t in summary['topics']:
    print(f"Topic {t['id']}: {', '.join(t['keywords'][:5])}")
```
