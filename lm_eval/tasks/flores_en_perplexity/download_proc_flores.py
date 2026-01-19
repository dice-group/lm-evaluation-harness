import os
import tarfile
import json
import pathlib
import urllib.request

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

def _process():
    """Create one JSON file per target language."""
    # download & extract
    _download_tar()
    _extract_tar()

    # paths inside the archive
    devtest_root = pathlib.Path(DS_DIR) / "devtest"
    eng_path = devtest_root / f"{COMMON_LANG}.devtest"

    # load English sentences
    eng_sentences = _load_lines(eng_path)

    # ensure output folder exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # process each language file
    for lang_file in devtest_root.iterdir():
        if lang_file.name == f"{COMMON_LANG}.devtest":
            continue

        lang_code = lang_file.stem
        target_sentences = _load_lines(lang_file)

        if len(target_sentences) != len(eng_sentences):
            raise ValueError(
                f"Line count mismatch: {lang_file.name} ({len(target_sentences)}) vs "
                f"{COMMON_LANG}.devtest ({len(eng_sentences)})"
            )

        data = []
        for eng, tgt in zip(eng_sentences, target_sentences):
            entry = {COMMON_LANG: eng, lang_code: tgt}
            data.append(entry)

        json_obj = {"data": data}

        out_path = pathlib.Path(OUTPUT_DIR) / f"{lang_code}-{COMMON_LANG}.json"
        with open(out_path, "w", encoding="utf-8") as out_f:
            json.dump(json_obj, out_f, ensure_ascii=False, indent=2)

        print(f"Wrote {out_path} ({len(data)} sentence pairs)")

if __name__ == "__main__":
    _process()