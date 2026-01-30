# Electronics Dataset Strategy: Sentiment Analysis & Recommendations

## Overview
This document outlines the strategy for preparing and using the Electronics.json dataset (~21M reviews) for sentiment analysis and recommendation systems with stratified sampling up to 300K reviews.

---

## 1. Stratified Sampling Approach

### Why Stratified Sampling?
- **Maintains distribution**: Ensures rating distribution is preserved (1★ to 5★)
- **Balanced representation**: Each rating category equally represented
- **Efficient data usage**: 300K reviews capture 1.4% of data with proportional representation
- **Reduced bias**: Prevents skewing towards high/low ratings

### Sampling Strategy
```
Original: ~21 million reviews
Sample: 300,000 reviews (1.4%)
Stratification: By overall rating (1-5 stars)

Example distribution (if proportional):
- 1★: ~3% → ~9,000 reviews
- 2★: ~5% → ~15,000 reviews
- 3★: ~12% → ~36,000 reviews
- 4★: ~25% → ~75,000 reviews
- 5★: ~55% → ~165,000 reviews
```

---

## 2. Data Preparation Process

### Step 1: Load & Analyze
- Read JSON lines format
- Identify all columns and data types
- Check rating distribution
- Detect missing values

### Step 2: Stratified Sampling
- Group by `overall` (rating) column
- Sample proportionally from each group
- Random state = 42 for reproducibility

### Step 3: Deduplication
- Remove duplicate reviews (same reviewer + product)
- Keep first occurrence (chronologically early)
- Removes ~2-5% of duplicates

### Step 4: Clean & Export
- Fill missing text with empty strings
- Remove rows with no review text
- Add metadata (review length, etc.)
- Export as CSV

---

## 3. Key Columns in Output CSV

| Column | Purpose | Type | Example |
|--------|---------|------|---------|
| `reviewerID` | Unique reviewer ID | String | A1N070NS9CJQ2I |
| `asin` | Product ID | String | 0060009810 |
| `overall` | Rating (1-5) | Float | 5.0 |
| `reviewText` | Full review text | String | "This product is great..." |
| `summary` | Review title | String | "Excellent!" |
| `reviewTime` | Review date | String | "07 17, 2002" |
| `verified` | Verified purchase | Boolean | true |
| `review_length` | Character count | Integer | 245 |

---

## 4. Use Cases

### Sentiment Analysis
```python
# Classify reviews as positive/negative/neutral
- Input: reviewText + summary
- Labels: overall rating (1-2★ negative, 3★ neutral, 4-5★ positive)
- Train models: logistic regression, BERT, TextBlob
```

### Recommendation System
```python
# Collaborative filtering or content-based
- User-Item matrix: reviewerID × asin with ratings
- Find similar users or products
- Predict ratings for unseen product-user pairs
```

### Product Analysis
```python
# Identify trends by product
- Group by asin
- Analyze sentiment over time
- Find most reviewed products
- Track rating changes
```

---

## 5. Data Quality Metrics

### Expected Statistics
- **Total reviews**: ~300,000 (after cleaning)
- **File size**: ~300-500 MB (CSV format)
- **Unique products**: ~50,000-100,000
- **Unique reviewers**: ~150,000-200,000
- **Avg review length**: 150-250 characters
- **Verified purchases**: ~85% of reviews

### Data Coverage
- Time span: 1995-2023 (historical data)
- All major product categories
- Geographic distribution: Mostly US/UK

---

## 6. Next Steps

### For Sentiment Analysis
1. Preprocess text (lowercase, remove special chars, tokenize)
2. Split data: 70% train, 15% validation, 15% test
3. Handle class imbalance (stratify splits)
4. Train models: Naive Bayes, SVM, Neural Networks
5. Evaluate with precision, recall, F1-score

### For Recommendations
1. Create user-product interaction matrix
2. Handle sparsity (300K reviews across 100K products)
3. Test models:
   - Item-based collaborative filtering
   - User-based collaborative filtering
   - Content-based (using sentiment features)
   - Hybrid approach
4. Evaluate using RMSE, MAE, precision@k

### For Streamlit App
- Load CSV in chunks
- Display filtered reviews by rating/sentiment
- Show product recommendations
- Visualize sentiment trends
- Real-time filtering and search

---

## 7. Performance Tips

### Memory Optimization
```python
# Read CSV in chunks
df = pd.read_csv('Electronics_sample_300k.csv', chunksize=10000)

# Use categorical for repeated values
df['overall'] = df['overall'].astype('category')
df['verified'] = df['verified'].astype('bool')
```

### Processing Speed
- Use pandas vectorized operations (not loops)
- Parallelize with multiprocessing for text processing
- Use sampling for model training initially
- Cache preprocessed data

### Storage
- CSV: ~300-500 MB
- Compressed (gzip): ~80-150 MB
- Parquet format: ~150-250 MB (faster loading)

---

## 8. Reproducibility

All operations use `random_state=42` for consistent results across runs.

To regenerate the same sample:
```bash
python prepare_data.py
```

This will create identical `Electronics_sample_300k.csv` on any machine.

---

## References
- Stratified sampling: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedShuffleSplit.html
- Sentiment analysis libraries: TextBlob, VADER, BERT
- Recommendation systems: Surprise library, Implicit
