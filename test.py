import pandas as pd
import spacy, os, re, itertools
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import networkx as nx

nlp = spacy.load("zh_core_web_sm")
os.makedirs("output", exist_ok=True)

def load_texts(path="data"):
    texts = {}
    for file in os.listdir(path):
        if file.endswith(".txt"):
            with open(os.path.join(path, file), "r", encoding="utf-8") as f:
                texts[file.replace(".txt", "")] = f.read()
    return texts

texts = load_texts()

def clean(doc):
    return [token.lemma_ for token in doc
            if not token.is_stop and token.pos_ in {"NOUN", "VERB", "ADJ"}]

docs = {k: nlp(v) for k, v in texts.items()}
cleaned = {k: " ".join(clean(doc)) for k, doc in docs.items()}

vec = TfidfVectorizer(max_features=100, ngram_range=(1,2))
X = vec.fit_transform(cleaned.values())
k = 6  
km = KMeans(n_clusters=k, random_state=42)
codes = km.fit_predict(X)

open_df = pd.DataFrame({"file": cleaned.keys(),
                        "raw": texts.values(),
                        "open_code": codes})
open_df.to_excel("output/open_coding.xlsx", index=False)

def co_occurrence(doc):
    sentences = [sent.text for sent in doc.sents]
    pairs = []
    for sent in sentences:
        words = re.findall(r"\b\w+\b", sent)
        pairs.extend(itertools.combinations(set(words), 2))
    return pairs

G = nx.Graph()
for doc in docs.values():
    for w1, w2 in co_occurrence(doc):
        if G.has_edge(w1, w2):
            G[w1][w2]["weight"] += 1
        else:
            G.add_edge(w1, w2, weight=1)

pr = nx.pagerank(G, weight="weight")
axial_keywords = [w for w, score in sorted(pr.items(), key=lambda x: x[1], reverse=True)[:30]]
axial_df = pd.DataFrame({"axial_keyword": axial_keywords,
                         "page_rank": [pr[w] for w in axial_keywords]})
axial_df.to_excel("output/axial_keywords.xlsx", index=False)


revenue_terms = {"收益", "分成", "订单", "收入", "门票", "研学费", "补贴"}
reproduction_terms = {"创新", "再创作", "设计", "釉色", "工时", "精力", "传承", "教学"}

def hit_terms(text, terms):
    return any(t in text for t in terms)

evidence = []
for file, raw in texts.items():
    has_rev = hit_terms(raw, revenue_terms)
    has_rep = hit_terms(raw, reproduction_terms)
    if has_rev and has_rep:
        sentences = [s for s in raw.split("。") if hit_terms(s, revenue_terms) or hit_terms(s, reproduction_terms)]
        evidence.append({"file": file,
                         "evidence": "。".join(sentences)})

evidence_df = pd.DataFrame(evidence)
evidence_df.to_excel("output/evidence_revenue_reproduction.xlsx", index=False)

print("complete")