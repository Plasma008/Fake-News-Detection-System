
import json

def cell(source, cell_type="code"):
    c = {
        "cell_type": cell_type,
        "metadata": {},
        "source": source if isinstance(source, list) else [source]
    }
    if cell_type == "code":
        c["execution_count"] = None
        c["outputs"] = []
    else:
        c["attachments"] = {}
    return c

cells = []

# Title
cells.append(cell([
    "# 📰 Fake News Detection System\n",
    "### CCNLP Advanced Learners - Problem Statement 1\n",
    "**Features:** Text Preprocessing · TF-IDF & N-Grams · ML Models Comparison · Evaluation Metrics · Confusion Matrix · Explainability"
], "markdown"))

# Install
cells.append(cell([
    "# Install required libraries\n",
    "import subprocess, sys\n",
    "pkgs = ['scikit-learn','pandas','numpy','matplotlib','seaborn','nltk','lime','wordcloud']\n",
    "for p in pkgs:\n",
    "    subprocess.run([sys.executable,'-m','pip','install',p,'-q'], check=False)"
]))

# Imports
cells.append(cell([
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import warnings, re, string\n",
    "warnings.filterwarnings('ignore')\n",
    "\n",
    "import nltk\n",
    "nltk.download('stopwords', quiet=True)\n",
    "nltk.download('punkt', quiet=True)\n",
    "from nltk.corpus import stopwords\n",
    "from nltk.stem import PorterStemmer\n",
    "\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.feature_extraction.text import TfidfVectorizer\n",
    "from sklearn.linear_model import LogisticRegression, PassiveAggressiveClassifier\n",
    "from sklearn.naive_bayes import MultinomialNB\n",
    "from sklearn.pipeline import Pipeline\n",
    "from sklearn.metrics import (\n",
    "    accuracy_score, precision_score, recall_score,\n",
    "    f1_score, classification_report, confusion_matrix\n",
    ")\n",
    "from sklearn.preprocessing import LabelEncoder\n",
    "import scipy.sparse as sp\n",
    "print('All imports successful!')"
]))

# Dataset creation
cells.append(cell([
    "## 1. Dataset Creation (Synthetic + Realistic)\n",
    "We create a realistic synthetic dataset covering various fake/real news topics."
], "markdown"))

cells.append(cell([
    "fake_headlines = [\n",
    "    'SHOCKING: Scientists Discover That Water Is Actually Dry According To New Study',\n",
    "    'Government Admits UFOs Control The Weather And Have Been For 50 Years',\n",
    "    'Bill Gates Microchip Found Inside COVID Vaccine By Concerned Mother',\n",
    "    '5G Towers Causing Mass Bird Deaths Scientists Refuse To Admit',\n",
    "    'Secret Cabal Of Elites Running The World From Underground Bunker',\n",
    "    'Drinking Bleach Cures Cancer Says Suppressed Doctor',\n",
    "    'Moon Landing Was Filmed In Hollywood Basement New Documents Reveal',\n",
    "    'Chemtrails Proven To Contain Mind Control Chemicals Study Finds',\n",
    "    'Deep State Planning To Replace All Humans With Robots By 2025',\n",
    "    'George Soros Funds Antifa To Overthrow American Democracy',\n",
    "    'Facebook Secretly Listening To Your Conversations To Sell You Products',\n",
    "    'Miracle Cure: Eating Raw Garlic Every Hour Eliminates All Diseases',\n",
    "    'NASA Hiding Proof Of Ancient Civilization On Mars From Public',\n",
    "    'Politician Caught Selling Babies To Satanic Cult In Pizza Shop Basement',\n",
    "    'Vaccines Cause Autism Proven By Whistleblower Doctor Who Fled Country',\n",
    "    'Scientists Admit Earth Is Flat But Are Forced To Stay Silent By Globalists',\n",
    "    'Leaked Documents Reveal Obama Was Born In Kenya And Is A Secret Muslim',\n",
    "    'New World Order Plans To Microchip Entire Population By 2030 Exposed',\n",
    "    'Hollywood Celebrities Running Child Trafficking Ring From Movie Sets',\n",
    "    'Aliens Abducted Entire Town In Nebraska Media Blackout In Effect',\n",
    "    'CURE FOUND: Lemon Juice Destroys Cancer Cells Doctors Dont Want You To Know',\n",
    "    'Robots Already Replaced 80 Percent Of Government Officials With AI Clones',\n",
    "    'Top Secret Operation Revealed: Sun Is Actually A Giant Projector',\n",
    "    'Exposed: Climate Change Is A Hoax Invented By Chinese Scientists For Profit',\n",
    "    'Breaking: Pope Francis Secretly A Reptilian Shapeshifter Vatican Insiders Claim',\n",
    "    'BOMBSHELL: Election Results Were Changed By Satellites Operated By Foreign Powers',\n",
    "    'Woke Agenda: Teachers Forced To Teach Children That Gravity Doesnt Exist',\n",
    "    'Secret Tunnels Under Major Cities Used By Elites For Illegal Activities Exposed',\n",
    "    'Mainstream Media Admits They Make Up Fake Stories To Control Population',\n",
    "    'Microplastics In Water Supply Part Of Population Control Plan Scientists Warn',\n",
    "]\n",
    "\n",
    "real_headlines = [\n",
    "    'Federal Reserve Raises Interest Rates By 25 Basis Points To Combat Inflation',\n",
    "    'NASA Artemis Mission Successfully Completes Lunar Orbit Test Flight',\n",
    "    'WHO Releases Updated Guidelines For COVID-19 Treatment Protocols',\n",
    "    'Scientists Develop New Battery Technology That Could Double Electric Vehicle Range',\n",
    "    'Congress Passes Bipartisan Infrastructure Bill Worth 1.2 Trillion Dollars',\n",
    "    'Climate Scientists Record Hottest Global Temperature In Recorded History',\n",
    "    'Apple Announces New iPhone With Advanced AI Features At Annual Event',\n",
    "    'United Nations Issues Warning About Growing Global Food Insecurity Crisis',\n",
    "    'Researchers Find New Evidence Of Ancient Roman Settlement In Britain',\n",
    "    'Stock Markets Rally After Positive Jobs Report Shows Unemployment Fell',\n",
    "    'European Union Passes Landmark Legislation On Artificial Intelligence Regulation',\n",
    "    'Scientists Successfully Edit Genes To Treat Rare Childhood Disease',\n",
    "    'Supreme Court Issues Ruling On Major Environmental Protection Case',\n",
    "    'World Health Organization Declares End Of Mpox Public Health Emergency',\n",
    "    'New Study Shows Regular Exercise Reduces Risk Of Heart Disease By 30 Percent',\n",
    "    'Government Releases Annual Budget Report Showing Deficit Reduction Progress',\n",
    "    'Astronomers Discover New Exoplanet In Habitable Zone Of Nearby Star',\n",
    "    'Major Tech Companies Agree To New Voluntary AI Safety Commitments',\n",
    "    'Tropical Storm Intensifies To Category 3 Hurricane As It Approaches Coast',\n",
    "    'Scientists Warn Arctic Ice Sheet Melting At Unprecedented Rate New Data Shows',\n",
    "    'Central Bank Holds Rates Steady Amid Economic Uncertainty Report Finds',\n",
    "    'New Alzheimer Drug Shows Promise In Large Scale Clinical Trial Results',\n",
    "    'Researchers Publish Study Linking Air Pollution To Increased Dementia Risk',\n",
    "    'International Space Station Celebrates 25 Years Of Continuous Human Habitation',\n",
    "    'Government Releases New Cybersecurity Framework For Critical Infrastructure',\n",
    "    'Economists Predict Moderate Growth Of 2.1 Percent For Coming Fiscal Year',\n",
    "    'Scientists Sequence Genome Of Newly Discovered Deep Sea Species',\n",
    "    'Major Earthquake Strikes Remote Region Rescue Operations Underway',\n",
    "    'New Report Shows Renewable Energy Now Cheaper Than Fossil Fuels In Most Markets',\n",
    "    'University Research Team Develops More Efficient Solar Panel Technology',\n",
    "]\n",
    "\n",
    "texts = fake_headlines + real_headlines\n",
    "labels = ['FAKE'] * len(fake_headlines) + ['REAL'] * len(real_headlines)\n",
    "\n",
    "df = pd.DataFrame({'text': texts, 'label': labels})\n",
    "df = df.sample(frac=1, random_state=42).reset_index(drop=True)\n",
    "print(f'Dataset size: {len(df)}')\n",
    "print(df['label'].value_counts())\n",
    "df.head()"
]))

# Preprocessing
cells.append(cell([
    "## 2. Text Preprocessing\n",
    "We clean text by removing punctuation, stopwords, and applying stemming."
], "markdown"))

cells.append(cell([
    "stemmer = PorterStemmer()\n",
    "stop_words = set(stopwords.words('english'))\n",
    "\n",
    "def preprocess_text(text):\n",
    "    text = text.lower()\n",
    "    text = re.sub(r'\\d+', '', text)\n",
    "    text = text.translate(str.maketrans('', '', string.punctuation))\n",
    "    tokens = text.split()\n",
    "    tokens = [stemmer.stem(t) for t in tokens if t not in stop_words and len(t) > 2]\n",
    "    return ' '.join(tokens)\n",
    "\n",
    "df['processed'] = df['text'].apply(preprocess_text)\n",
    "\n",
    "print('Original:  ', df['text'][0])\n",
    "print('Processed: ', df['processed'][0])"
]))

# Feature Extraction
cells.append(cell([
    "## 3. Feature Extraction - TF-IDF with N-Grams\n",
    "We use TF-IDF with unigrams, bigrams, and trigrams."
], "markdown"))

cells.append(cell([
    "le = LabelEncoder()\n",
    "y = le.fit_transform(df['label'])  # FAKE=0, REAL=1\n",
    "X = df['processed']\n",
    "\n",
    "X_train, X_test, y_train, y_test = train_test_split(\n",
    "    X, y, test_size=0.25, random_state=42, stratify=y\n",
    ")\n",
    "\n",
    "# TF-IDF Vectorizers with different n-gram ranges\n",
    "tfidf_unigram = TfidfVectorizer(ngram_range=(1,1), max_features=5000)\n",
    "tfidf_bigram  = TfidfVectorizer(ngram_range=(1,2), max_features=8000)\n",
    "tfidf_trigram = TfidfVectorizer(ngram_range=(1,3), max_features=10000)\n",
    "\n",
    "X_train_uni = tfidf_unigram.fit_transform(X_train)\n",
    "X_test_uni  = tfidf_unigram.transform(X_test)\n",
    "\n",
    "X_train_bi = tfidf_bigram.fit_transform(X_train)\n",
    "X_test_bi  = tfidf_bigram.transform(X_test)\n",
    "\n",
    "X_train_tri = tfidf_trigram.fit_transform(X_train)\n",
    "X_test_tri  = tfidf_trigram.transform(X_test)\n",
    "\n",
    "print(f'Train size: {X_train.shape[0]}, Test size: {X_test.shape[0]}')\n",
    "print(f'Unigram features: {X_train_uni.shape[1]}')\n",
    "print(f'Bigram features:  {X_train_bi.shape[1]}')\n",
    "print(f'Trigram features: {X_train_tri.shape[1]}')"
]))

# Model Training
cells.append(cell([
    "## 4. Model Training & Comparison\n",
    "We train 3 models: Logistic Regression, Passive Aggressive Classifier, and Naive Bayes."
], "markdown"))

cells.append(cell([
    "models = {\n",
    "    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),\n",
    "    'Passive Aggressive': PassiveAggressiveClassifier(max_iter=1000, random_state=42),\n",
    "    'Naive Bayes': MultinomialNB(alpha=0.1),\n",
    "}\n",
    "\n",
    "feature_sets = {\n",
    "    'Unigram': (X_train_uni, X_test_uni),\n",
    "    'Bigram':  (X_train_bi,  X_test_bi),\n",
    "    'Trigram': (X_train_tri, X_test_tri),\n",
    "}\n",
    "\n",
    "results = []\n",
    "\n",
    "for feat_name, (X_tr, X_te) in feature_sets.items():\n",
    "    for model_name, model in models.items():\n",
    "        model.fit(X_tr, y_train)\n",
    "        preds = model.predict(X_te)\n",
    "        results.append({\n",
    "            'Features': feat_name,\n",
    "            'Model': model_name,\n",
    "            'Accuracy':  round(accuracy_score(y_test, preds)*100, 2),\n",
    "            'Precision': round(precision_score(y_test, preds, zero_division=0)*100, 2),\n",
    "            'Recall':    round(recall_score(y_test, preds, zero_division=0)*100, 2),\n",
    "            'F1':        round(f1_score(y_test, preds, zero_division=0)*100, 2),\n",
    "        })\n",
    "\n",
    "results_df = pd.DataFrame(results)\n",
    "print(results_df.to_string(index=False))"
]))

# Visualization
cells.append(cell([
    "## 5. Performance Visualization"
], "markdown"))

cells.append(cell([
    "fig, axes = plt.subplots(1, 2, figsize=(16, 6))\n",
    "fig.suptitle('Model Performance Comparison', fontsize=16, fontweight='bold')\n",
    "\n",
    "# Accuracy heatmap\n",
    "pivot = results_df.pivot(index='Model', columns='Features', values='Accuracy')\n",
    "sns.heatmap(pivot, annot=True, fmt='.1f', cmap='YlOrRd', ax=axes[0],\n",
    "            linewidths=0.5, cbar_kws={'label': 'Accuracy %'})\n",
    "axes[0].set_title('Accuracy (%) by Model & Feature Type', fontweight='bold')\n",
    "\n",
    "# F1 bar chart\n",
    "colors = ['#2196F3','#FF5722','#4CAF50']\n",
    "best_per_model = results_df.loc[results_df.groupby('Model')['F1'].idxmax()]\n",
    "bars = axes[1].bar(best_per_model['Model'], best_per_model['F1'],\n",
    "                   color=colors, edgecolor='black', linewidth=0.8)\n",
    "for bar, val in zip(bars, best_per_model['F1']):\n",
    "    axes[1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,\n",
    "                 f'{val}%', ha='center', va='bottom', fontweight='bold')\n",
    "axes[1].set_title('Best F1-Score per Model', fontweight='bold')\n",
    "axes[1].set_ylabel('F1-Score (%)')\n",
    "axes[1].set_ylim(0, 115)\n",
    "axes[1].tick_params(axis='x', rotation=15)\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
]))

# Best model + confusion matrix
cells.append(cell([
    "## 6. Best Model - Detailed Evaluation & Confusion Matrix"
], "markdown"))

cells.append(cell([
    "# Find best model configuration\n",
    "best_row = results_df.loc[results_df['Accuracy'].idxmax()]\n",
    "print(f\"Best Model: {best_row['Model']} with {best_row['Features']} features\")\n",
    "print(f\"Accuracy: {best_row['Accuracy']}%  F1: {best_row['F1']}%\")\n",
    "\n",
    "# Retrain best model\n",
    "feat_map = {'Unigram': (X_train_uni, X_test_uni, tfidf_unigram),\n",
    "            'Bigram':  (X_train_bi,  X_test_bi,  tfidf_bigram),\n",
    "            'Trigram': (X_train_tri, X_test_tri, tfidf_trigram)}\n",
    "best_feat = best_row['Features']\n",
    "X_tr_best, X_te_best, best_vectorizer = feat_map[best_feat]\n",
    "\n",
    "model_map = {\n",
    "    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),\n",
    "    'Passive Aggressive': PassiveAggressiveClassifier(max_iter=1000, random_state=42),\n",
    "    'Naive Bayes': MultinomialNB(alpha=0.1),\n",
    "}\n",
    "best_model = model_map[best_row['Model']]\n",
    "best_model.fit(X_tr_best, y_train)\n",
    "best_preds = best_model.predict(X_te_best)\n",
    "\n",
    "print('\\nClassification Report:')\n",
    "print(classification_report(y_test, best_preds, target_names=['FAKE','REAL']))\n",
    "\n",
    "# Confusion Matrix\n",
    "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
    "\n",
    "cm = confusion_matrix(y_test, best_preds)\n",
    "sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0],\n",
    "            xticklabels=['FAKE','REAL'], yticklabels=['FAKE','REAL'],\n",
    "            linewidths=1, linecolor='gray')\n",
    "axes[0].set_title(f'Confusion Matrix\\n({best_row[\"Model\"]} + {best_feat})', fontweight='bold')\n",
    "axes[0].set_xlabel('Predicted Label')\n",
    "axes[0].set_ylabel('True Label')\n",
    "\n",
    "# Metrics radar\n",
    "metrics = ['Accuracy','Precision','Recall','F1']\n",
    "vals = [best_row[m] for m in metrics]\n",
    "x = np.arange(len(metrics))\n",
    "bars2 = axes[1].bar(x, vals, color=['#3F51B5','#E91E63','#FF9800','#4CAF50'],\n",
    "                    edgecolor='black', linewidth=0.7)\n",
    "for bar, v in zip(bars2, vals):\n",
    "    axes[1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,\n",
    "                 f'{v}%', ha='center', fontweight='bold')\n",
    "axes[1].set_xticks(x)\n",
    "axes[1].set_xticklabels(metrics)\n",
    "axes[1].set_ylim(0, 115)\n",
    "axes[1].set_title('Best Model Metrics Summary', fontweight='bold')\n",
    "axes[1].set_ylabel('Score (%)')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
]))

# Explainability
cells.append(cell([
    "## 7. Model Explainability - Top Contributing Features\n",
    "We analyze which words/n-grams are most influential in predicting FAKE vs REAL news."
], "markdown"))

cells.append(cell([
    "def explain_model(model, vectorizer, top_n=15):\n",
    "    feature_names = vectorizer.get_feature_names_out()\n",
    "    \n",
    "    if hasattr(model, 'coef_'):\n",
    "        coef = model.coef_.flatten()\n",
    "        top_fake_idx = np.argsort(coef)[:top_n]\n",
    "        top_real_idx = np.argsort(coef)[-top_n:][::-1]\n",
    "        fake_words = [(feature_names[i], coef[i]) for i in top_fake_idx]\n",
    "        real_words = [(feature_names[i], coef[i]) for i in top_real_idx]\n",
    "    elif hasattr(model, 'feature_log_prob_'):\n",
    "        log_prob = model.feature_log_prob_\n",
    "        diff = log_prob[0] - log_prob[1]\n",
    "        top_fake_idx = np.argsort(diff)[-top_n:][::-1]\n",
    "        top_real_idx = np.argsort(diff)[:top_n]\n",
    "        fake_words = [(feature_names[i], diff[i]) for i in top_fake_idx]\n",
    "        real_words = [(feature_names[i], abs(diff[i])) for i in top_real_idx]\n",
    "    else:\n",
    "        print('Model does not support feature importance.')\n",
    "        return\n",
    "    \n",
    "    fig, axes = plt.subplots(1, 2, figsize=(16, 6))\n",
    "    fig.suptitle('Top Features Driving Predictions', fontsize=14, fontweight='bold')\n",
    "    \n",
    "    fw, fv = zip(*fake_words)\n",
    "    rw, rv = zip(*real_words)\n",
    "    \n",
    "    axes[0].barh(fw, [abs(v) for v in fv], color='#EF5350')\n",
    "    axes[0].set_title('Top FAKE News Indicators', color='#C62828', fontweight='bold')\n",
    "    axes[0].set_xlabel('Feature Weight')\n",
    "    axes[0].invert_yaxis()\n",
    "    \n",
    "    axes[1].barh(rw, rv, color='#66BB6A')\n",
    "    axes[1].set_title('Top REAL News Indicators', color='#2E7D32', fontweight='bold')\n",
    "    axes[1].set_xlabel('Feature Weight')\n",
    "    axes[1].invert_yaxis()\n",
    "    \n",
    "    plt.tight_layout()\n",
    "    plt.show()\n",
    "\n",
    "explain_model(best_model, best_vectorizer)"
]))

# Word cloud
cells.append(cell([
    "## 8. Word Clouds - Fake vs Real News Vocabulary"
], "markdown"))

cells.append(cell([
    "try:\n",
    "    from wordcloud import WordCloud\n",
    "    fake_text = ' '.join(df[df['label']=='FAKE']['processed'])\n",
    "    real_text = ' '.join(df[df['label']=='REAL']['processed'])\n",
    "\n",
    "    fig, axes = plt.subplots(1, 2, figsize=(16, 6))\n",
    "    \n",
    "    wc_fake = WordCloud(width=800, height=400, background_color='white',\n",
    "                        colormap='Reds', max_words=80).generate(fake_text)\n",
    "    axes[0].imshow(wc_fake, interpolation='bilinear')\n",
    "    axes[0].axis('off')\n",
    "    axes[0].set_title('FAKE News - Word Cloud', fontsize=14, fontweight='bold', color='#C62828')\n",
    "    \n",
    "    wc_real = WordCloud(width=800, height=400, background_color='white',\n",
    "                        colormap='Greens', max_words=80).generate(real_text)\n",
    "    axes[1].imshow(wc_real, interpolation='bilinear')\n",
    "    axes[1].axis('off')\n",
    "    axes[1].set_title('REAL News - Word Cloud', fontsize=14, fontweight='bold', color='#2E7D32')\n",
    "    \n",
    "    plt.suptitle('Vocabulary Distribution', fontsize=16, fontweight='bold')\n",
    "    plt.tight_layout()\n",
    "    plt.show()\n",
    "except ImportError:\n",
    "    print('WordCloud not available, skipping...')"
]))

# Live prediction
cells.append(cell([
    "## 9. Live Prediction Function"
], "markdown"))

cells.append(cell([
    "def predict_news(text, model=best_model, vectorizer=best_vectorizer):\n",
    "    processed = preprocess_text(text)\n",
    "    vec = vectorizer.transform([processed])\n",
    "    pred = model.predict(vec)[0]\n",
    "    label = le.inverse_transform([pred])[0]\n",
    "    \n",
    "    if hasattr(model, 'predict_proba'):\n",
    "        prob = model.predict_proba(vec)[0]\n",
    "        confidence = max(prob) * 100\n",
    "    elif hasattr(model, 'decision_function'):\n",
    "        score = abs(model.decision_function(vec)[0])\n",
    "        confidence = min(99, 50 + score * 20)\n",
    "    else:\n",
    "        confidence = 75.0\n",
    "    \n",
    "    emoji = '🚨 FAKE' if label == 'FAKE' else '✅ REAL'\n",
    "    print(f'Headline: {text[:80]}...' if len(text)>80 else f'Headline: {text}')\n",
    "    print(f'Prediction: {emoji} | Confidence: {confidence:.1f}%')\n",
    "    print('-'*60)\n",
    "    return label, confidence\n",
    "\n",
    "# Test examples\n",
    "test_samples = [\n",
    "    'Scientists Discover Drinking Coffee Every Day Prevents All Types Of Cancer Forever',\n",
    "    'Federal Reserve Raises Interest Rates By Half A Percentage Point To Control Inflation',\n",
    "    'SHOCKING: Government Is Secretly Putting Fluoride In Water To Control Your Mind',\n",
    "    'New Climate Report Shows Carbon Emissions Rose By 1.5 Percent Last Year',\n",
    "]\n",
    "\n",
    "print('=== FAKE NEWS DETECTOR - LIVE PREDICTIONS ===')\n",
    "print('='*60)\n",
    "for sample in test_samples:\n",
    "    predict_news(sample)"
]))

# Summary
cells.append(cell([
    "## 10. Summary\n",
    "| Component | Implementation |\n",
    "|-----------|---------------|\n",
    "| **Preprocessing** | Lowercasing, punctuation removal, stopword filtering, stemming |\n",
    "| **Feature Extraction** | TF-IDF with Unigram, Bigram & Trigram N-grams |\n",
    "| **Models Trained** | Logistic Regression, Passive Aggressive Classifier, Naive Bayes |\n",
    "| **Evaluation Metrics** | Accuracy, Precision, Recall, F1-Score, Confusion Matrix |\n",
    "| **Explainability** | Top feature weights per class (FAKE/REAL indicators) |\n",
    "| **Visualization** | Heatmaps, Bar charts, Word Clouds, Confusion Matrix |\n",
    "| **Live Prediction** | Text → Preprocess → Vectorize → Predict → Confidence Score |"
], "markdown"))

nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.9.0"}
    },
    "cells": cells
}

with open('fake_news_detection.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print('Notebook 1 created: fake_news_detection.ipynb')
