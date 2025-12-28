from sklearn.metrics import precision_score, recall_score
from nltk.translate.bleu_score import sentence_bleu
from rouge_score import rouge_scorer
import time

# ------------------ Sample Data ---------------
# ---
# Correct expected responses (ground truth)
reference_answers = [
    "Mutual funds pool money from investors and invest in securities.",
    "Income tax is calculated on your annual income as per tax slabs.",
    "SIP allows investing a fixed amount regularly in mutual funds."
]

# Model-generated answers
predicted_answers = [
    "Mutual funds collect money from people and invest in stocks and bonds.",
    "Income tax depends on yearly income and slab rates declared by govt.",
    "SIP lets you invest fixed money regularly into mutual funds."
]

# Binary relevance for retrieval evaluation
# 1 = relevant answer, 0 = irrelevant
actual_relevance = [1, 1, 1]
predicted_relevance = [1, 1, 1]

# ------------------ Precision & Recall ------------------
precision = precision_score(actual_relevance, predicted_relevance)
recall = recall_score(actual_relevance, predicted_relevance)

print("Precision:", precision)
print("Recall:", recall)

# ------------------ BLEU Score ------------------
for ref, pred in zip(reference_answers, predicted_answers):
    bleu = sentence_bleu([ref.split()], pred.split())
    print("BLEU Score:", bleu)

# ------------------ ROUGE Score ------------------
scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)

for ref, pred in zip(reference_answers, predicted_answers):
    scores = scorer.score(ref, pred)
    print("ROUGE-1:", scores['rouge1'].fmeasure)
    print("ROUGE-L:", scores['rougeL'].fmeasure)

# ------------------ Response Time Testing ------------------
start = time.time()

# simulate model call here
_ = "Model generates answer"    # your LLM response

end = time.time()
print("Response Time:", end - start, "seconds")
