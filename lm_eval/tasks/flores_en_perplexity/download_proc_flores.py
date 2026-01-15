# Write logic to download: https://tinyurl.com/flores200dataset as flores200_dataset.tar.gz
# Then inside this tar, read English file in devtest/ directory where filename is eng_Latn.devtest
# Then inside this tar, loop through each file in devtest/ directory where filenames are like <flores_lang_code>.devtest
# For each file create a local json that is in format: {"test": {"data": [{"eng_Latn": "<content of 1st line>", "<target_lang>": "<content of 1st line>"}, ...]}}
# This is for translation task