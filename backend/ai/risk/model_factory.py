from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

CLASS_WEIGHTS = {
    "baixo": 1,
    "medio": 2,
    "alto": 4,
    "critico": 6
}

def create_pipeline():
    return Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=5000,
            min_df=2,
            max_df=0.9,
            sublinear_tf=True,
            strip_accents="unicode"
        )),
        ("clf", LogisticRegression(
            C=0.6,
            penalty="l2",
            class_weight=CLASS_WEIGHTS,
            max_iter=2000,
            solver="lbfgs",
            n_jobs=1
        ))
    ])