from io import TextIOWrapper
import re
from nltk import download as nltk_download
from nltk import RegexpTokenizer, FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from googletrans import Translator
import statistics

nltk_download('punkt')
nltk_download('stopwords')
nltk_download('vader_lexicon')


def open_file(file_name: str) -> TextIOWrapper:
    """Opens text file inside folder with the name provided.

    Args:
        file_name (str): name of a given file inside the folder

    Returns:
        TextIOWrapper: content of the file specified
    """
    text_file = open(file_name, 'r')
    return text_file


def get_email_list(text_file: TextIOWrapper) -> list:
    """Gets emails inside a text file.

    Args:
        text_file (TextIOWrapper): content of a given file

    Returns:
        list: list of emails found
    """
    email_regex = re.compile(r'[a-z0-9]+@[a-z0-9]+\.[a-z]+')
    email_list = [re.search(email_regex, line).group(0)
                  for line in text_file if re.search(email_regex, line)]
    return email_list


def get_usernames(email_list: list) -> list:
    """Gets usernames inside a list of emails.

    Args:
        email_list (list): list of emails

    Returns:
        list: list of usernames found
    """
    unique_email_set = set(email_list)

    username_list = [username.split('@')[0] for username in unique_email_set]
    return username_list


def get_domains(email_list: list) -> dict:
    """Gets domains and frequency inside a list of emails.

    Args:
        email_list (list): list of emails

    Returns:
        dict: dict with the domains as keys and frequency as values
    """
    domain_list = [domain.split('@')[1:][0] for domain in email_list]

    domain_dict = dict.fromkeys(domain_list, 0)

    for domain in domain_list:
        if domain in domain_list:
            domain_dict[domain] += 1

    return domain_dict


def get_word_list(text_file: TextIOWrapper) -> list:
    """Gets only the words inside a text file.

    Args:
        text_file (TextIOWrapper): content of a given file

    Returns:
        list: list of words inside a text file
    """
    word_list = list()
    reg_tokenizer = RegexpTokenizer(r"\w+")

    for line in text_file:
        lower_line = line.lower()
        word_list.extend(reg_tokenizer.tokenize(lower_line))

    return word_list


def get_filtered_words(text_file: TextIOWrapper) -> list:
    """Filters words from stopwords inside a text file.

    Args:
        text_file (TextIOWrapper): content of a given file

    Returns:
        list: list of filtered words inside a text file
    """
    word_list = get_word_list(text_file)
    stop_words = set(stopwords.words("portuguese"))
    filtered_list = [
        word for word in word_list if word.casefold() not in stop_words]
    return filtered_list


def get_common_words(text_file: TextIOWrapper, number: int) -> list:
    """Get frequency of words inside a text file.

    Args:
        text_file (TextIOWrapper): content of a given file
        number (int): number of most commons words to be retrieved

    Returns:
        list: list of the most frequent words inside a text file
    """
    filtered_list = get_filtered_words(text_file)
    word_frequency_list = FreqDist(filtered_list)

    return word_frequency_list.most_common(number)


def get_token_count(text_file: TextIOWrapper) -> int:
    """Gets number of tokens inside a text file.

    Args:
        text_file (TextIOWrapper): content of a given file

    Returns:
        int: number of tokens inside a text file
    """
    filtered_list = get_filtered_words(text_file)
    return len(filtered_list)


def get_word_count(text_file: TextIOWrapper) -> int:
    """Gets number of words inside a text file.

    Args:
        text_file (TextIOWrapper): content of a given file

    Returns:
        int: number of words inside a text file
    """
    word_list = get_word_list(text_file)
    return len(word_list)


def get_character_count(text_file: TextIOWrapper) -> int:
    """Gets number of characters inside a text file.

    Args:
        text_file (TextIOWrapper): content of a given file

    Returns:
        int: number of characters inside a text file
    """
    text = text_file.read()
    return len(text)


def get_sentiment(text_file: TextIOWrapper) -> tuple:
    """Calculates sentiment score of a given text file and returns
    if it is positive, neutral or negative.

    Args:
        text_file (TextIOWrapper): content of a given file

    Returns:
        tuple: text sentiment string and the score number
    """
    sid = SentimentIntensityAnalyzer()
    translator = Translator()

    sentence_list = [sent_tokenize(line, "portuguese") for line in text_file]
    compound_score_list = list()

    for phrase_list in sentence_list:
        if len(phrase_list) > 0:
            def translate(phrase): return translator.translate(
                phrase, src='pt', dest='en').text
            sentiment_score = [sid.polarity_scores(
                translate(phrase)) for phrase in phrase_list]
            score_dict_list = [foo.get('compound') for foo in sentiment_score]
            compound_score_list.append(statistics.mean(score_dict_list))

    text_sentiment_score = statistics.mean(compound_score_list)

    if text_sentiment_score > 0:
        text_sentiment = "positivo"
    elif text_sentiment_score < 0:
        text_sentiment = "negativo"
    else:
        text_sentiment = "neutro"

    return (text_sentiment, text_sentiment_score)
