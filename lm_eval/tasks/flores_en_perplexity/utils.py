## logic based on: lm_eval/tasks/wikitext/wikitext.yaml
import re
import datasets

# lm_eval --model hf \
#     --model_args pretrained=EleutherAI/gpt-j-6B \
#     --tasks flores_en_perplexity \
#     --device cuda:0 \
#     --batch_size 8
    

## Writes out an example input from the dataset with 1-shot
# python -m scripts.write_out \
#     --output_base_path /data/nikit_ws/repos/lm-evaluation-harness/lm_eval/tasks/flores_en_perplexity/sample_out \
#     --tasks flores_en_perplexity \
#     --sets test

    
# def preprocess(text):
#     text = text.strip()
#     #text = re.sub("\\[.*?\\]", "", text)
#     text = text.replace("  ", " ")
#     return text

# def process_docs(dataset: datasets.Dataset) -> datasets.Dataset:
#     def _process_doc(doc):
#         out_doc = {
#             "input": preprocess(f"German: {doc["deu_Latn"]} \nEnglish: "),
#             "output": preprocess(doc["eng_Latn"]),
#         }
#         print(f'out_doc requested: {out_doc}')
#         return out_doc

#     return dataset.map(_process_doc)

# def doc_to_target(doc) -> str:
#     return doc["output"]

# def process_results(doc, results):
#     (loglikelihood,) = results
#     #print(f'Loglikelihood: {loglikelihood}')
#     _words = len(re.split(r"\s+", doc_to_target(doc)))
#     _bytes = len(doc_to_target(doc).encode("utf-8"))
#     #print(f"perplexity: {math.exp(-loglikelihood / _words)}")
#     return {
#         "word_perplexity": (loglikelihood, _words),
#         "byte_perplexity": (loglikelihood, _bytes),
#         "bits_per_byte": (loglikelihood, _bytes),
#     }