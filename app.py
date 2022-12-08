import re
from nltk import download as nltk_download
from nltk import RegexpTokenizer, FreqDist
from nltk.corpus import stopwords

nltk_download('punkt')
nltk_download('stopwords')

file = open('text.txt', 'r')

email_regex = re.compile(r'[a-z0-9]+@[a-z0-9]+\.[a-z]+')
email_list = [re.search(email_regex, line).group(0) for line in file if re.search(email_regex, line)]

unique_email_set = set(email_list)

username_list = [username.split('@')[0] for username in unique_email_set]
print(username_list)

domain_list = [domain.split('@')[1:][0] for domain in email_list]


domain_dict = dict.fromkeys(domain_list, 0)

for domain in domain_list:
    if domain in domain_list:
        domain_dict[domain] += 1

print(domain_dict)

word_list = list()
tokenizer = RegexpTokenizer(r"\w+")

for line in file:
    lower_line = line.lower()
    word_list.extend(tokenizer.tokenize(lower_line))

print(len(word_list))
merged_text = ' '.join(word_list)
print(len(merged_text))

stop_words = set(stopwords.words("portuguese"))


filtered_list = [word for word in word_list if word.casefold() not in stop_words]

print(len(filtered_list))

word_frequency_list = FreqDist(filtered_list)

print(word_frequency_list.most_common(8))