import random
import sys
import os
from collections import defaultdict

#SET DEFAULT CONFIG
TEXT_SOURCE = "text/moby_dick.txt"
K_GRAM = 1


def load_words(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read().lower()
    return [word for word in text.split() if word.isalpha()]

# creates a list for each word - mimicing possible probabilities
def build_kgram_markov_chain(words, k=2):
    if k < 1:
        raise ValueError("k must be > 0")
    markov = defaultdict(list)
    for i in range(len(words) - k):
        prefix = tuple(words[i:i + k])
        next_word = words[i + k]
        markov[prefix].append(next_word)
    return markov

# generate text by randomly choosing a word from correspnding word's list, repeat
def generate_kgram_text(markov, length, k=2, start_prefix=None):
    if not markov:
        return ""

    if not start_prefix or start_prefix not in markov:
        start_prefix = random.choice(list(markov.keys()))
    output = list(start_prefix)

    for _ in range(length - k):
        prefix = tuple(output[-k:])
        next_words = markov.get(prefix)
        if not next_words:
            prefix = random.choice(list(markov.keys()))
            next_words = markov[prefix]
        output.append(random.choice(next_words))

    return ' '.join(output)

# command line args provided for scripting if neccessary
filename = sys.argv[1] if len(sys.argv) > 1 else TEXT_SOURCE
k = int(sys.argv[2]) if len(sys.argv) > 2 else K_GRAM  # default: bigram

tokens = load_words(filename)
model = build_kgram_markov_chain(tokens, k=k)
generated = generate_kgram_text(model, length=len(tokens), k=k)

# save to file here
output_filename = f"text/generated_markov_k{k}_{os.path.splitext(os.path.basename(filename))[0]}.txt"

with open(output_filename, 'w', encoding='utf-8') as out:
    out.write(generated)

print(f"\nGenerated text saved to: {output_filename}")
