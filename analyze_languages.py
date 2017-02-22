import json
from collections import defaultdict

if __name__ == '__main__':
  with open('languages.json') as data_file:
    data = json.load(data_file)
    print(len(data))

    lang_byte_count = defaultdict(int)

    for repo in data:
      for lang, byte_count in repo['languages'].items():
        print('{0},{1}'.format(lang, byte_count))
        lang_byte_count[lang] += int(byte_count) 
    print(lang_byte_count)
