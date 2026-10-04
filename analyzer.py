import re

FAKE_KEYWORDS = {
    "shocking": 3,
    "breaking": 2,
    "exposed": 3,
    "secret": 3,
    "miracle": 4,
    "scandal": 3,
    "urgent": 2,
    "viral": 2,
    "unbelievable": 4,
    "you won't believe": 4,
    "100% true": 4,
    "guaranteed": 3,
    "they don't want you to know": 5,
    "hidden truth": 4,
    "share immediately": 4,
    "government hiding": 4,
    "censored": 3,
    "conspiracy": 3,
}

RELIABLE_KEYWORDS = {
    "according to": 2,
    "official": 2,
    "report": 1,
    "research": 2,
    "study": 2,
    "data": 1,
    "statement": 1,
    "ministry": 1,
    "government": 1,
    "university": 1,
    "published": 2,
}


def analyze_text(text):
    text_lower = text.lower()

    fake_matches = []
    reliable_matches = []

    fake_score = 0
    reliable_score = 0

    for keyword, weight in FAKE_KEYWORDS.items():
        if keyword in text_lower:
            fake_matches.append(keyword)
            fake_score += weight

    for keyword, weight in RELIABLE_KEYWORDS.items():
        if keyword in text_lower:
            reliable_matches.append(keyword)
            reliable_score += weight

    words = re.findall(r"\b[\w'-]+\b", text)
    sentences = re.split(r"[.!?]+", text)
    sentences = [s for s in sentences if s.strip()]

    exclamation_count = text.count("!")
    question_count = text.count("?")
    capital_words = sum(
        1 for word in words
        if len(word) > 2 and word.isupper()
    )

    if exclamation_count >= 3:
        fake_score += 2

    if capital_words >= 3:
        fake_score += 2

    total_score = fake_score - reliable_score

    if total_score >= 8:
        result = "Likely Fake"
        level = "danger"
    elif total_score >= 4:
        result = "Suspicious"
        level = "warning"
    else:
        result = "Likely Reliable"
        level = "safe"

    max_score = max(fake_score + reliable_score, 1)
    risk_percentage = min(
        round((fake_score / max_score) * 100),
        100
    )

    reasons = []

    if fake_matches:
        reasons.append(
            "Emotionally loaded or suspicious keywords were detected."
        )

    if exclamation_count >= 3:
        reasons.append(
            "The text contains many exclamation marks."
        )

    if capital_words >= 3:
        reasons.append(
            "Multiple words are written in capital letters."
        )

    if reliable_matches:
        reasons.append(
            "Some reporting or evidence-related terms were detected."
        )

    if not reasons:
        reasons.append(
            "No strong fake-news keyword patterns were detected."
        )

    return {
        "result": result,
        "level": level,
        "fake_score": fake_score,
        "reliable_score": reliable_score,
        "risk_percentage": risk_percentage,
        "fake_keywords": fake_matches,
        "reliable_keywords": reliable_matches,
        "word_count": len(words),
        "sentence_count": len(sentences),
        "exclamation_count": exclamation_count,
        "question_count": question_count,
        "reasons": reasons
    }