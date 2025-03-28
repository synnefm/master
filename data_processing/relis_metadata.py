import os
import json
from collections import Counter, defaultdict
from statistics import mean, median
from datetime import datetime

# ----- Helper functions ----- #

def parse_date(date_str):
    """
    Try to parse a date in the expected format: dd.mm.yyyy.
    Return a datetime object or None if parsing fails.
    """
    try:
        return datetime.strptime(date_str, "%d.%m.%Y")
    except Exception:
        return None

# ----- Construct the file path ----- #

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, '..', '..', 'data', 'RELIS', 'q&a.jsonl')
file_path = os.path.abspath(file_path)

# ----- Read all JSON objects ----- #

documents = []
with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        doc = json.loads(line)
        documents.append(doc)

print("Total documents in the file:", len(documents))

# ----- Language Statistics ----- #

language_values = [doc.get("Language") for doc in documents if "Language" in doc]
language_counts = Counter(language_values)

print("\nUnique 'Language' values and their counts:")
print(f"Total unique languages: {len(language_counts)}")
for language, count in language_counts.items():
    print(f"{language}: {count}")

# ----- Example: Documents with Language 'ca' ----- #

print("\nDocument(s) with Language == 'ca':")
for doc in documents:
    if doc.get("Language") == "ca":
        print(json.dumps(doc, indent=2))

# ----- Answer Length Statistics ----- #

# Extract all answer lengths.
answer_lengths = [len(doc.get("Answer", "")) for doc in documents]

if answer_lengths:
    overall_mean = mean(answer_lengths)
    overall_median = median(answer_lengths)
else:
    overall_mean = overall_median = 0

print("\nOverall Answer Length Statistics:")
print(f"Mean (average) answer length: {overall_mean:.2f} characters")
print(f"Median answer length: {overall_median} characters")

# Per-language answer length stats.
language_stats = defaultdict(list)
for doc in documents:
    lang = doc.get("Language", "unknown")
    answer = doc.get("Answer", "")
    language_stats[lang].append(len(answer))

print("\nPer-language Answer Length Statistics:")
print(f"{'Language':<10} {'Count':<6} {'Mean':<10} {'Median':<10}")
for lang, lengths in language_stats.items():
    lang_mean = mean(lengths) if lengths else 0
    lang_median = median(lengths) if lengths else 0
    print(f"{lang:<10} {len(lengths):<6} {lang_mean:<10.2f} {lang_median:<10}")

# ----- Short Answer Analysis ----- #
# Define bins (in characters) for answer lengths.
bins = [(0, 50), (51, 100), (101, 200), (201, 500), (501, 1000), (1001, 2000), (2001, float('inf'))]
bin_labels = [
    "0-50", "51-100", "101-200", "201-500", "501-1000", "1001-2000", "2001+"
]
bin_counts = {label: 0 for label in bin_labels}

for length in answer_lengths:
    for (low, high), label in zip(bins, bin_labels):
        if low <= length <= high:
            bin_counts[label] += 1
            break

print("\nAnswer Length Distribution:")
for label in bin_labels:
    count = bin_counts[label]
    percentage = (count / len(answer_lengths)) * 100 if answer_lengths else 0
    print(f"{label:10s}: {count:5d} documents ({percentage:5.2f}%)")

# The below printout demonstrates that very few documents have extremely short answers,
# which supports the idea that nearly all 36,000 documents can be useful.

# ----- Shortest Answers Example ----- #

sorted_docs = sorted(documents, key=lambda d: len(d.get("Answer", "")))
print("\nTen documents with the shortest 'Answer' fields:")
for idx, doc in enumerate(sorted_docs[:10], start=1):
    answer_length = len(doc.get("Answer", ""))
    print(f"\nDocument {idx} (Answer length: {answer_length} characters):")
    print(json.dumps(doc, indent=2))

# ----- Find an document with answer length that fits in appendex ----- #

filtered_docs = [
    doc for doc in documents 
    if len(doc.get("Answer", "")) < overall_mean
]

if filtered_docs:
    # Sort the filtered documents by closeness to the mean (from below)
    sorted_filtered = sorted(filtered_docs, key=lambda d: overall_mean - len(d.get("Answer", "")))
    
    target_doc = sorted_filtered[8000]
    print("\nExample document with an answer a little under the average length (Language: en):")
    print(json.dumps(target_doc, indent=2))

else:
    print("No document found with an answer length below the average and language 'en'.")

# ----- Publication Date Range ----- #

dates = []
for doc in documents:
    pub_date = parse_date(doc.get("Published", ""))
    if pub_date:
        dates.append(pub_date)

if dates:
    earliest = min(dates)
    latest = max(dates)
    print("\nPublication Date Range:")
    print("Earliest:", earliest.strftime("%d.%m.%Y"))
    print("Latest:  ", latest.strftime("%d.%m.%Y"))
else:
    print("\nNo valid publication dates found.")

