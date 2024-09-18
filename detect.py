def levenshtein_distance(str1, str2):
    str1, str2 = str1.lower(), str2.lower()
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
    max_dist = max(0, max(len1, len2) // 2 - 1)
    match1 = [False] * len1
    match2 = [False] * len2
    matches = 0
    transpositions = 0
    for i in range(len1):
        start = max(0, i - max_dist)
        end = min(i + max_dist + 1, len2)
        for j in range(start, end):
            if match2[j] or s1[i] != s2[j]:
                continue
            match1[i] = match2[j] = True
            matches += 1
            break
    if matches == 0:
        return 0.0
    k = 0
    for i in range(len1):
        if not match1[i]:
            continue
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

def string_similarity(str1, str2):
    return {"levenshtein": levenshtein_similarity(str1, str2), "jaroWinkler": jaro_winkler_similarity(str1, str2)}

def determine_match_type(str1, str2):
    similarity = string_similarity(str1, str2)
    weighted_similarity = (float(similarity["levenshtein"]) * 0.4) + (float(similarity["jaroWinkler"]) * 0.6)
    if weighted_similarity >= 95:
        return "Full Match"
    elif weighted_similarity >= 80:
        return "Strong Partial Match"
    elif weighted_similarity >= 60:
        return "Partial Match"
    elif weighted_similarity >= 40:
        return "Weak Partial Match"
    else:
        return "No Significant Match"

str1 = "1730 7th st nw washington dc 20001"
str2 = "1730 7th St NW Apt 411, Washington, DC 20001"
print(f"Match Type: {determine_match_type(str1, str2)}")
