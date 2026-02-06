def explain_decision(model, texto, top_k=5):
    pipeline = model.base_estimator

    vectorizer = pipeline.named_steps["tfidf"]
    classifier = pipeline.named_steps["clf"]

    tfidf = vectorizer.transform([texto])

    classe_prevista = classifier.predict([texto])[0]
    class_idx = classifier.classes_.tolist().index(classe_prevista)

    coef = classifier.coef_

    scores = tfidf.toarray()[0] * coef[class_idx]
    features = vectorizer.get_feature_names_out()

    top = sorted(
        zip(features, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [t for t, s in top[:top_k] if s > 0]