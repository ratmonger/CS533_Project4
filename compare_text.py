import numpy as np
import random
from collections import Counter
import matplotlib.pyplot as plt
import os
import sys
from scipy.stats import chi2_contingency

#CONFIG - CHANGE TEXT SAMPLES HERE
DEFAULT_TEXT_A = 'text/moby_dick.txt'
DEFAULT_TEXT_B = 'text/frankenstein.txt'
PLOT_DIR = 'plots'
os.makedirs(PLOT_DIR, exist_ok=True)

PERMUTATION_TRIALS = 100 #first baseline permutation test, generate this many permutations just once
BOOTSTRAP_TRIALS = 100 #runs this many simple comparisons - each comparison is using 2 texts made by resampling
P_VAL_TRIALS = 100 #how many p values to collect?
P_VAL_PERMUTATIONS_PER_TRIAL =100 #how many permutations to run for a single p value?



if len(sys.argv) >= 3:
    file_a = sys.argv[1]
    file_b = sys.argv[2]
else:
    file_a = DEFAULT_TEXT_A
    file_b = DEFAULT_TEXT_B

#set filename and set name used in plots
basename = os.path.splitext(os.path.basename(file_a))[0] + "_vs_" + os.path.splitext(os.path.basename(file_b))[0]
plotname = os.path.splitext(os.path.basename(file_a))[0] + "_vs_" + os.path.splitext(os.path.basename(file_b))[0]

#loading data here
def load_and_tokenize(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read().lower()
    return [word for word in text.split() if word.isalpha()]

tokens_a = load_and_tokenize(file_a)
tokens_b = load_and_tokenize(file_b)


def get_normalized_freq(tokens, vocab=None):
    counter = Counter(tokens)
    if vocab is None:
        vocab = set(counter.keys())
    total = sum(counter.values())
    freq = {word: counter[word] / total for word in vocab}
    for word in vocab:
        freq.setdefault(word, 0.0)
    return np.array([freq[word] for word in sorted(vocab)])

def distribution_distance(fa, fb):
    return np.sum(np.abs(fa - fb))  # L1 distance provided by bruna


vocab = set(tokens_a).union(tokens_b)
freq_a = get_normalized_freq(tokens_a, vocab)
freq_b = get_normalized_freq(tokens_b, vocab)
phi_actual = distribution_distance(freq_a, freq_b)

def permutation_test(tokens_a, tokens_b, num_trials=1000):
    combined = tokens_a + tokens_b
    len_a = len(tokens_a)
    phi_perms = []
    for _ in range(num_trials):
        random.shuffle(combined)
        perm_a = combined[:len_a]
        perm_b = combined[len_a:]
        fa_perm = get_normalized_freq(perm_a, vocab)
        fb_perm = get_normalized_freq(perm_b, vocab)
        phi = distribution_distance(fa_perm, fb_perm)
        phi_perms.append(phi)
    return np.array(phi_perms)

phi_null = permutation_test(tokens_a, tokens_b, num_trials=PERMUTATION_TRIALS)
p_val = np.mean(phi_null >= phi_actual)

lower = np.percentile(phi_null, 2.5)
upper = np.percentile(phi_null, 97.5)

print(f"Observed φ: {phi_actual:.4f}")
print(f"Permutation test p-value: {p_val:.4f}")
print(f"95% CI under null: [{lower:.4f}, {upper:.4f}]")

#Permutation Histogram
plt.figure()
plt.hist(phi_null, bins=30, alpha=0.7, label='Permutation φ')
plt.axvline(phi_actual, color='red', linestyle='--', label='Actual φ')
plt.xlabel('Distribution Difference (φ)')
plt.ylabel('Frequency')
plt.legend()
plt.title("Permutation Test on Word Distributions: " + basename)
plt.savefig(f"{PLOT_DIR}/permutation_{basename}.png")
plt.close()

#BOOT STRAPPING
def bootstrap_phi(tokens_a, tokens_b, vocab, n_trials=BOOTSTRAP_TRIALS):
    phi_values = []
    for _ in range(n_trials):
        sample_a = random.choices(tokens_a, k=len(tokens_a))
        sample_b = random.choices(tokens_b, k=len(tokens_b))
        freq_a = get_normalized_freq(sample_a, vocab)
        freq_b = get_normalized_freq(sample_b, vocab)
        phi_values.append(distribution_distance(freq_a, freq_b))
    return np.array(phi_values)


phi_bootstrap = bootstrap_phi(tokens_a, tokens_b, vocab)
mean_phi = np.mean(phi_bootstrap)
se_phi = np.std(phi_bootstrap, ddof=1)
ci_lower = np.percentile(phi_bootstrap, 2.5)
ci_upper = np.percentile(phi_bootstrap, 97.5)

print(f"Bootstrap Mean φ: {mean_phi:.4f}")
print(f"Bootstrap SE: {se_phi:.4f}")
print(f"Bootstrap 95% CI for φ: [{ci_lower:.4f}, {ci_upper:.4f}]")

#Bootstrap Histogram
plt.figure()
plt.hist(phi_bootstrap, bins=30, alpha=0.7, color='orange', label='Bootstrap φ')
plt.axvline(phi_actual, color='red', linestyle='--', label='Actual φ')
plt.xlabel('Distribution Difference (φ)')
plt.ylabel('Frequency')
plt.legend()
plt.title("Bootstrap Distribution of φ: " + basename)
plt.savefig(f"{PLOT_DIR}/bootstrap_{basename}.png")
plt.close()

#RUN MANY PERMUTATION, GET MANY P-VAL
def collect_p_values(tokens_a, tokens_b, n_experiments=P_VAL_TRIALS, n_perms=P_VAL_PERMUTATIONS_PER_TRIAL):
    p_values = []
    for _ in range(n_experiments):
        a_sample = random.choices(tokens_a, k=len(tokens_a))
        b_sample = random.choices(tokens_b, k=len(tokens_b))
        vocab = set(a_sample).union(b_sample)
        fa = get_normalized_freq(a_sample, vocab)
        fb = get_normalized_freq(b_sample, vocab)
        phi_obs = distribution_distance(fa, fb)

        phi_null = []
        combined = a_sample + b_sample
        len_a = len(a_sample)
        for _ in range(n_perms):
            random.shuffle(combined)
            pa = combined[:len_a]
            pb = combined[len_a:]
            fa_perm = get_normalized_freq(pa, vocab)
            fb_perm = get_normalized_freq(pb, vocab)
            phi_null.append(distribution_distance(fa_perm, fb_perm))

        p_val = np.mean(np.array(phi_null) >= phi_obs)
        p_values.append(p_val)
    return p_values



p_vals = collect_p_values(tokens_a, tokens_b, n_experiments=100, n_perms=100)

#P Value Histogram
plt.figure()
plt.hist(p_vals, bins=20, edgecolor='black', alpha=0.7)
plt.xlabel("p-value")
plt.ylabel("Frequency")
plt.title("Histogram of Permutation Test p-values: " + basename)
plt.axvline(0.05, color='red', linestyle='--', label='α = 0.05')
plt.legend()
plt.savefig(f"{PLOT_DIR}/pvals_{basename}.png")
plt.close()




print("\n=== CHI-SQUARED TEST OF INDEPENDENCE ===")

#contingency table
vocab = sorted(list(set(tokens_a).union(tokens_b)))
word_to_index = {word: i for i, word in enumerate(vocab)}
table = np.zeros((2, len(vocab)), dtype=int)

# word occurrences for both books
count_a = Counter(tokens_a)
count_b = Counter(tokens_b)

for word, idx in word_to_index.items():
    table[0, idx] = count_a.get(word, 0)
    table[1, idx] = count_b.get(word, 0)

#chi squared test
chi2_stat, p_val, dof, expected = chi2_contingency(table)

print(f"Chi-squared statistic: {chi2_stat:.4f}")
print(f"Degrees of freedom: {dof}")
print(f"p-value: {p_val:.6f}")

# top 10 words by contribution
contrib = (table - expected) ** 2 / expected
word_contrib = np.sum(contrib, axis=0)
top_indices = np.argsort(word_contrib)[-10:][::-1]
print("\nTop contributing words:")
for idx in top_indices:
    print(f"{vocab[idx]:<15} contribution: {word_contrib[idx]:.4f}")


#Bar plot for top contributing words
top_n = 10
top_indices = np.argsort(word_contrib)[-top_n:][::-1]
top_words = [vocab[i] for i in top_indices]
top_values = [word_contrib[i] for i in top_indices]

plt.figure(figsize=(10, 6))
plt.bar(top_words, top_values, color='teal')
plt.xlabel('Word')
plt.ylabel('Chi-squared Contribution')
plt.title(f'Top {top_n} Contributing Words: ' + basename)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/chi2_top_words_{basename}.png")
plt.close()

