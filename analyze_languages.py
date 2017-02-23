import json
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns

if __name__ == '__main__':
  with open('languages.json') as data_file:
    data = json.load(data_file)
    print(len(data))

    lang_byte_count = defaultdict(int)

    for repo in data:
      for lang, byte_count in repo['languages'].items():
        lang_byte_count[lang] += int(byte_count) 

    lang_df = pd.DataFrame.from_dict(lang_byte_count, orient='index')
    lang_df.columns = ['bytes']
    lang_df['languages'] = lang_df.index
    lang_df.sort_values('bytes',ascending=True, inplace=True)

    sns_plot = sns.barplot(x='languages', y='bytes', data=lang_df,
    estimator=sum)

    for i in sns_plot.get_xticklabels():
      i.set_rotation(90)

    plt.ticklabel_format(style='plain', axis='y',useOffset=False)
    plt.title('Languages by total bytes')

    sns_plot.figure.savefig('langs.png', bbox_inches='tight')
