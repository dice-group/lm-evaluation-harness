## FLORES 200 - Perplexity

This task is meant for base-pretrained models to test their understanding of different languages in a translation setting. We use the FLORES200 dataset (https://github.com/facebookresearch/flores/tree/main/flores200) for this task. This task computes word_perplexity, byte_perplexity and bits_per_byte (https://huggingface.co/docs/lighteval/en/metric-list) and aggregates them using the default logic. By default we choose English as common language for the translation task and provide evaluation configs for both directions. The common langauge can be changed in [gen_flores_config.py](gen_flores_config.py).

To download the dataset and generate config files:
```bash
python -m lm_eval.tasks.flores_en_perplexity.gen_flores_config
```
To run a config:
```bash
lm_eval --model hf --model_args pretrained=EleutherAI/gpt-j-6B --tasks flores_en_perplexity_eng_Latn-deu_Latn --device cuda:0 --batch_size 8
```