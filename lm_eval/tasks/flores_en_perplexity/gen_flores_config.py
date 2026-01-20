import os
import tarfile
import json
import pathlib
import urllib.request
import csv
import textwrap

COMMON_LANG="eng_Latn"

DATA_URL = "https://tinyurl.com/flores200dataset"
TAR_NAME = "./lm_eval/tasks/flores_en_perplexity/flores200_dataset.tar.gz"
EXTRACT_ROOT_DIR = "./lm_eval/tasks/flores_en_perplexity/"
FLORES_DS_DIR_NAME = "flores200_dataset"
DS_DIR = os.path.join(EXTRACT_ROOT_DIR, FLORES_DS_DIR_NAME)
OUTPUT_DIR = "./lm_eval/tasks/flores_en_perplexity/flores_json"

def _download_tar():
    """Download the tarball if missing."""
    if not os.path.exists(TAR_NAME):
        print(f"Downloading {DATA_URL} → {TAR_NAME}")
        urllib.request.urlretrieve(DATA_URL, TAR_NAME)
    else:
        print(f"{TAR_NAME} already exists")

def _extract_tar():
    """Extract the tarball if not already extracted."""
    if not os.path.isdir(DS_DIR):
        print(f"Extracting {TAR_NAME} → {EXTRACT_ROOT_DIR}")
        with tarfile.open(TAR_NAME, "r:gz") as tar:
            tar.extractall(EXTRACT_ROOT_DIR)
    else:
        print(f"{EXTRACT_ROOT_DIR} already extracted")

def _load_lines(file_path):
    """Read a text file and return stripped lines."""
    with open(file_path, encoding="utf-8") as f:
        return [ln.strip() for ln in f.readlines()]
    
def preprocess(text):
    text = text.strip()
    #text = re.sub("\\[.*?\\]", "", text)
    text = text.replace("  ", " ")
    return text

def _load_lang_names(tsv_path: str) -> dict[str, str]:
    """
    Reads ``flores200_codes.tsv`` (expected columns: Language, FLORES-200 code)
    and returns a mapping from FLORES‑200 code → readable language name.
    """
    mapping = {}
    with open(tsv_path, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            if len(row) != 2:
                continue      # skip malformed lines / header
            name, code = row
            mapping[code.strip()] = name.strip()
    return mapping

def gen_save_yaml(src_lang_code, src_lang_name, tgt_lang_code, tgt_lang_name, config_dir, test_json_path):
    yaml_content_to_cl = textwrap.dedent(f"""\
        task: flores_en_perplexity_{src_lang_code}-{tgt_lang_code}
        dataset_kwargs:
            data_files:
            test: {test_json_path.as_posix()}
            field: data
        doc_to_target: "{{{{{tgt_lang_code}}}}}"
        doc_to_text: "{src_lang_name}: {{{{{src_lang_code}}}}} \\n{tgt_lang_name}: "
        include: ../flores_perplexity_common
        """)

    yaml_path = config_dir / f"flores_en_perplexity_{src_lang_code}-{tgt_lang_code}.yaml"
    with open(yaml_path, "w", encoding="utf-8") as yml_f:
        yml_f.write(yaml_content_to_cl)

    print(f"Wrote config {yaml_path}")

def _process():
    """Create one JSON file per target language **and** a matching YAML config."""
    # download & extract
    _download_tar()
    _extract_tar()

    # paths inside the archive
    devtest_root = pathlib.Path(DS_DIR) / "devtest"
    eng_path = devtest_root / f"{COMMON_LANG}.devtest"

    # load English sentences
    eng_sentences = _load_lines(eng_path)

    # ensure output folders exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    config_dir = pathlib.Path(EXTRACT_ROOT_DIR) / "configs"
    config_dir.mkdir(parents=True, exist_ok=True)

    # load the language‑code → name map (the TSV lives next to this script)
    tsv_path = os.path.join(EXTRACT_ROOT_DIR, "flores200_codes.tsv")
    code_to_name = _load_lang_names(str(tsv_path))
    
    
    cl_lang_name = code_to_name.get(COMMON_LANG, COMMON_LANG)

    # process each language file
    for lang_file in devtest_root.iterdir():
        if lang_file.name == f"{COMMON_LANG}.devtest":
            continue

        lang_code = lang_file.stem                # e.g. "deu_Latn"
        target_sentences = _load_lines(lang_file)

        if len(target_sentences) != len(eng_sentences):
            raise ValueError(
                f"Line count mismatch: {lang_file.name} ({len(target_sentences)}) vs "
                f"{COMMON_LANG}.devtest ({len(eng_sentences)})"
            )

        data = []
        for eng, tgt in zip(eng_sentences, target_sentences):
            entry = {COMMON_LANG: preprocess(eng), lang_code: preprocess(tgt)}
            data.append(entry)

        json_obj = {"data": data}
        json_path = pathlib.Path(OUTPUT_DIR) / f"{lang_code}-{COMMON_LANG}.json"
        with open(json_path, "w", encoding="utf-8") as out_f:
            json.dump(json_obj, out_f, ensure_ascii=False, indent=2)

        print(f"Wrote {json_path} ({len(data)} sentence pairs)")

        # Human‑readable language name (fallback to the code if not found)
        lang_name = code_to_name.get(lang_code, lang_code)

        # saving yaml in both directions
        gen_save_yaml(lang_code, lang_name, COMMON_LANG, cl_lang_name, config_dir, json_path)
        gen_save_yaml(COMMON_LANG, cl_lang_name, lang_code, lang_name, config_dir, json_path)

if __name__ == "__main__":
    _process()