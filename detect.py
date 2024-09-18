import math

def levenshtein_distance(str1, str2):
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i-1][j-1] if str1[i-1] == str2[j-1] else min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + 1)
    return dp[m][n]

def levenshtein_similarity(str1, str2):
    distance = levenshtein_distance(str1, str2)
    max_length = max(len(str1), len(str2))
    return 100 if max_length == 0 else round(((max_length - distance) / max_length * 100), 2)

def jaro_winkler(s1, s2):
    jaro = jaro_distance(s1, s2)
    return jaro + (common_prefix_length(s1, s2) * 0.1 * (1 - jaro))

def jaro_distance(s1, s2):
    if s1 == s2:
        return 1.0
    len1, len2 = len(s1), len(s2)
    max_dist = max(len1, len2) // 2 - 1
    match1 = [False] * len1
    match2 = [False] * len2
    matches = 0
    transpositions = 0
    for i in range(len1):
        start = max(0, i - max_dist)
        end = min(i + max_dist + 1, len2)
        for j in range(start, end):
            if not match2[j] and s1[i] == s2[j]:
                match1[i] = match2[j] = True
                matches += 1
                break
    if matches == 0:
        return 0.0
    k = 0
    for i in range(len1):
        if match1[i]:
            while not match2[k]:
                k += 1
            if s1[i] != s2[k]:
                transpositions += 1
            k += 1
    return (matches / len1 + matches / len2 + (matches - transpositions / 2) / matches) / 3.0

def common_prefix_length(s1, s2):
    i = 0
    while i < min(len(s1), len(s2)) and s1[i] == s2[i]:
        i += 1
    return min(i, 4)

def jaro_winkler_similarity(str1, str2):
    return round(jaro_winkler(str1.lower(), str2.lower()) * 100, 2)

def cosine_similarity(str1, str2):
    words1 = str1.lower().split()
    words2 = str2.lower().split()
    unique_words = set(words1 + words2)
    vector1 = [words1.count(word) for word in unique_words]
    vector2 = [words2.count(word) for word in unique_words]
    dot_product = sum(v1 * v2 for v1, v2 in zip(vector1, vector2))
    magnitude1 = math.sqrt(sum(v * v for v in vector1))
    magnitude2 = math.sqrt(sum(v * v for v in vector2))
    return dot_product / (magnitude1 * magnitude2)

def n_gram_similarity(str1, str2, n=2):
    def get_n_grams(s, n):
        return set(s[i:i+n] for i in range(len(s) - n + 1))
    
    ngrams1 = get_n_grams(str1.lower(), n)
    ngrams2 = get_n_grams(str2.lower(), n)
    intersection = ngrams1.intersection(ngrams2)
    union = ngrams1.union(ngrams2)
    return len(intersection) / len(union)

def string_similarity(str1, str2):
    str1 = str1.lower()
    str2 = str2.lower()
    return {
        'levenshtein': levenshtein_similarity(str1, str2),
        'jaroWinkler': jaro_winkler_similarity(str1, str2),
        'cosine': round(cosine_similarity(str1, str2) * 100, 2),
        'nGram': round(n_gram_similarity(str1, str2, 2) * 100, 2),
    }

def determine_match_type(str1, str2):
    similarity = string_similarity(str1, str2)
    weighted_similarity = (
        float(similarity['levenshtein']) * 0.15 +
        float(similarity['jaroWinkler']) * 0.40 +
        float(similarity['cosine']) * 0.25 +
        float(similarity['nGram']) * 0.20
    )
    if weighted_similarity >= 95:
        return "Full Match"
    if weighted_similarity >= 75:
        return "Strong Partial Match"
    if weighted_similarity >= 55:
        return "Partial Match"
    if weighted_similarity >= 40:
        return "Weak Partial Match"
    return "No Significant Match"

# Example usage
str1 = "Apt 411 Washington DC 20001"
str2 = "1730 7th St NW Apt 411, Washington, DC 20001"
print(f"Match Type: {determine_match_type(str1, str2)}")
print(f"Similarity Scores: {string_similarity(str1, str2)}")
