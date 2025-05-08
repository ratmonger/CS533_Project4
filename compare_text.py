import numpy as np
import random
from collections import Counter
import matplotlib.pyplot as plt





def load_and_tokenize(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read().lower()
    tokens = [word for word in text.split() if word.isalpha()] ## grab words only
    return tokens

tokens_a = load_and_tokenize('text/moby_dick.txt')
tokens_b = load_and_tokenize('text/frankenstein.txt')

#normalized frequency counter
def get_normalized_freq(tokens, vocab=None):
    counter = Counter(tokens)
    if vocab is None:
        vocab = set(counter.keys())
    total = sum(counter.values())
    freq = {word: counter[word]/total for word in vocab}
    
    for word in vocab:
        freq.setdefault(word, 0.0) #by default words have freq 0
    return np.array([freq[word] for word in sorted(vocab)])

# combine the words of both books
vocab = set(tokens_a).union(set(tokens_b))
freq_a = get_normalized_freq(tokens_a, vocab)
freq_b = get_normalized_freq(tokens_b, vocab)

def distribution_distance(fa, fb):
    return np.sum(np.abs(fa - fb))  #L1 distance bruna reccomended

phi_actual = distribution_distance(freq_a, freq_b)

#   Permutation testing
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

phi_null = permutation_test(tokens_a, tokens_b, num_trials=100)


p_val = np.mean(phi_null >= phi_actual)
print(f"Observed φ: {phi_actual:.4f}")
print(f"Permutation test p-value: {p_val:.4f}")

lower = np.percentile(phi_null, 2.5)
upper = np.percentile(phi_null, 97.5)
print(f"95% CI under null: [{lower:.4f}, {upper:.4f}]")


# histogram of distance between permutations
plt.hist(phi_null, bins=30, alpha=0.7, label='Permutation φ')
plt.axvline(phi_actual, color='red', linestyle='--', label='Actual φ')
plt.xlabel('Distribution Difference (φ)')
plt.ylabel('Frequency')
plt.legend()
plt.title('Permutation Test on Word Distributions')
plt.show()

###################################################################
###  BOOTSTRAP
###################################################################


def bootstrap_phi(tokens_a, tokens_b, vocab, n_trials=100):
    phi_values = []

    for _ in range(n_trials):
        sample_a = random.choices(tokens_a, k=len(tokens_a))
        sample_b = random.choices(tokens_b, k=len(tokens_b))
        
        freq_a = get_normalized_freq(sample_a, vocab)
        freq_b = get_normalized_freq(sample_b, vocab)
        
        phi = distribution_distance(freq_a, freq_b)
        phi_values.append(phi)
    
    return np.array(phi_values)

phi_bootstrap = bootstrap_phi(tokens_a, tokens_b, vocab)

# summary statistics
mean_phi = np.mean(phi_bootstrap)
se_phi = np.std(phi_bootstrap, ddof=1) 

ci_lower = np.percentile(phi_bootstrap, 2.5)
ci_upper = np.percentile(phi_bootstrap, 97.5)

print(f"Bootstrap Mean φ: {mean_phi:.4f}")
print(f"Bootstrap SE: {se_phi:.4f}")
print(f"Bootstrap 95% CI for φ: [{ci_lower:.4f}, {ci_upper:.4f}]")


# -------------- P-VALUE ACCUMULATION ACROSS TRIALS ------------------
def collect_p_values(tokens_a, tokens_b, n_experiments=100, n_perms=100):
    p_values = []

    for _ in range(n_experiments):
        # Optionally: resample tokens to simulate variability
        a_sample = random.choices(tokens_a, k=len(tokens_a))
        b_sample = random.choices(tokens_b, k=len(tokens_b))

        # Build vocab for this run
        vocab = set(a_sample).union(b_sample)
        fa = get_normalized_freq(a_sample, vocab)
        fb = get_normalized_freq(b_sample, vocab)
        phi_obs = distribution_distance(fa, fb)

        # Permutation test
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

        # Calculate p-value
        p_val = np.mean(np.array(phi_null) >= phi_obs)
        p_values.append(p_val)
    
    return p_values

# Run collection
p_vals = collect_p_values(tokens_a, tokens_b, n_experiments=100, n_perms=100)

# Plot
plt.hist(p_vals, bins=20, edgecolor='black', alpha=0.7)
plt.xlabel("p-value")
plt.ylabel("Frequency")
plt.title("Histogram of Permutation Test p-values")
plt.axvline(0.05, color='red', linestyle='--', label='α = 0.05')
plt.legend()
plt.show()
