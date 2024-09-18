function levenshteinDistance(str1, str2) {
    str1 = str1.toLowerCase(); str2 = str2.toLowerCase();
    const m = str1.length, n = str2.length;
    const dp = Array(m + 1).fill().map(() => Array(n + 1).fill(0));
    for (let i = 0; i <= m; i++) dp[i][0] = i;
    for (let j = 0; j <= n; j++) dp[0][j] = j;
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            dp[i][j] = str1[i - 1] === str2[j - 1] ? dp[i - 1][j - 1] : Math.min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + 1);
        }
    }
    return dp[m][n];
}

function levenshteinSimilarity(str1, str2) {
    const distance = levenshteinDistance(str1, str2);
    const maxLength = Math.max(str1.length, str2.length);
    return maxLength === 0 ? 100 : ((maxLength - distance) / maxLength * 100).toFixed(2);
}

function jaroWinkler(s1, s2) {
    const jaro = jaroDistance(s1, s2);
    return jaro + (commonPrefixLength(s1, s2) * 0.1 * (1 - jaro));
}

function jaroDistance(s1, s2) {
    if (s1 === s2) return 1.0;
    const len1 = s1.length, len2 = s2.length;
    const maxDist = Math.floor(Math.max(len1, len2) / 2) - 1;
    const match1 = new Array(len1).fill(false), match2 = new Array(len2).fill(false);
    let matches = 0, transpositions = 0;
    for (let i = 0; i < len1; i++) {
        const start = Math.max(0, i - maxDist), end = Math.min(i + maxDist + 1, len2);
        for (let j = start; j < end; j++) {
            if (match2[j] || s1[i] !== s2[j]) continue;
            match1[i] = match2[j] = true; matches++; break;
        }
    }
    if (matches === 0) return 0.0;
    let k = 0;
    for (let i = 0; i < len1; i++) {
        if (!match1[i]) continue;
        while (!match2[k]) k++;
        if (s1[i] !== s2[k]) transpositions++;
        k++;
    }
    return (matches / len1 + matches / len2 + (matches - transpositions / 2) / matches) / 3.0;
}

function commonPrefixLength(s1, s2) {
    let i = 0;
    while (i < Math.min(s1.length, s2.length) && s1[i] === s2[i]) i++;
    return Math.min(i, 4);
}

function jaroWinklerSimilarity(str1, str2) {
    return (jaroWinkler(str1.toLowerCase(), str2.toLowerCase()) * 100).toFixed(2);
}

function stringSimilarity(str1, str2) {
    return { levenshtein: levenshteinSimilarity(str1, str2), jaroWinkler: jaroWinklerSimilarity(str1, str2) };
}

function determineMatchType(str1, str2) {
    const similarity = stringSimilarity(str1, str2);
    const weightedSimilarity = (parseFloat(similarity.levenshtein) * 0.4) + (parseFloat(similarity.jaroWinkler) * 0.6);
    if (weightedSimilarity >= 95) return "Full Match";
    if (weightedSimilarity >= 80) return "Strong Partial Match";
    if (weightedSimilarity >= 60) return "Partial Match";
    if (weightedSimilarity >= 40) return "Weak Partial Match";
    return "No Significant Match";
}

const str1 = "1730 7th st nw washington dc 20001";
const str2 = "1730 7th St NW Apt 411, Washington, DC 20001";
console.log(`Match Type: ${determineMatchType(str1, str2)}`);
