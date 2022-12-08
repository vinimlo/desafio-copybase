import text_analyzer

print()

text_file = text_analyzer.open_file('text.txt')
email_list = text_analyzer.get_email_list(text_file)

username_list = text_analyzer.get_usernames(email_list)
print(f"Usernames: {username_list}")

domain_dict = text_analyzer.get_domains(email_list)
print(f"Domínios com frequência: {domain_dict}")

text_file = text_analyzer.open_file('text.txt')
number_of_words = 8
frequent_words = text_analyzer.get_common_words(text_file, number_of_words)
print(f"{number_of_words} palavras mais comuns: {frequent_words}")

text_file = text_analyzer.open_file('text.txt')
sentiment = text_analyzer.get_sentiment(text_file)
print(f"Sentimento do texto com pontuação: {sentiment}")

text_file = text_analyzer.open_file('text.txt')
tokens_count = text_analyzer.get_token_count(text_file)
print(f"Quantidade de tokens: {tokens_count}")

text_file = text_analyzer.open_file('text.txt')
word_count = text_analyzer.get_word_count(text_file)
print(f"Quantidade de palavras: {word_count}")

text_file = text_analyzer.open_file('text.txt')
char_count = text_analyzer.get_character_count(text_file)
print(f"Quantidade de caracteres: {char_count}")