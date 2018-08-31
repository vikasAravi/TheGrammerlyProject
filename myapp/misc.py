# import nltk
# from nltk.corpus import stopwords
# import enchant
# import re
# import json,requests

# # def score_calculator(essay):
# #     features_dict = {"score": 0}
# #     d1 = enchant.Dict("en-US")
# #     d2 = enchant.Dict("en-GB")
# #     stop_words = set(stopwords.words('english'))

# #     # spelling mistakes, pos count, average sentence length, average word length, words greater than k characters
# #     # word count, word count excluding stop words, grammar mistakes
# #     spelling_mistakes = 0
# #     word_count_minus_stopwords = 0
# #     word_count = 0
# #     # cleaned_essay = re.sub(r"[.,?!;:]", "", essay)
    
# #     for word in words:
# #         if d1.check(word) == False:
# #             if d2.check(word) == False:
# #                 print(word)
# #                 spelling_mistakes += 1
# #         else:
# #             pos = nltk.pos_tag([word])[0][1][:2]
# #             if pos not in features_dict:
# #                 features_dict[pos] = 1
# #             else:
# #                 features_dict[pos] += 1
# #             if word not in stop_words:
# #                 word_count_minus_stopwords += 1
# #         word_count += 1
# #     features_dict["spelling_mistakes"] = spelling_mistakes
# #     features_dict["word_count"] = word_count
# #     features_dict["word_count_minus_stopwords"] = word_count_minus_stopwords

# #     # grammar mistakes
# #     features_dict["grammar_errors"] = len(re.findall(r",[A-Za-z]", essay)) + len(
# #         re.findall(r"\.[A-Za-z]", essay)) + len(re.findall(r"\.[a-z]", essay)) + len(re.findall(r"\. [a-z]", essay))

# #     if word_count // 150:  # 150 word limit
# #         features_dict["score"] = 10 - ((spelling_mistakes * 0.5) + (features_dict["grammar_errors"] * 0.25))
# #         if features_dict["score"] < 0:
# #             features_dict["score"]=0
# #         # generate score with ml??

# #     return {"score": features_dict["score"], "grammar_errors": features_dict["grammar_errors"],
# #             "spelling_errors": features_dict["spelling_mistakes"], "word_count":features_dict["word_count"]}

# def score_calculator(essay):
#     features_dict = {"score": 0}
#     stop_words = set(stopwords.words('english'))

#     # spelling mistakes, pos count, average sentence length, average word length, words greater than k characters
#     # word count, word count excluding stop words, grammar mistakes
#     word_count_minus_stopwords = 0
#     # cleaned_essay = re.sub(r"[.,?!;:]", "", essay)
#     # words = re.sub(r"[.,?!;():\"\']", " ", essay).split()
#     # word_count = 0
#     tmp = re.sub(r"[.,?!;():\"\']", " ", essay).split()
#     word_count = len(tmp)
#     url = 'http://localhost:8082/v2/check'
#     payload = {"text":essay,"language":"en-US", "enabledOnly":"false"}
# #headers = {'charset': 'utf-8'}
#     response = requests.post(url,data = payload)
#     T = response.json()['matches']
#     # print(T) #gives the response body in the API
#     count = 0
#     spelling_mistakes = 0
#     grammar_errors = 0
#     list_of_errors = []
#     l = []
#     #list_of_offsets = []
#     for i in range(0,len(T)):
#         s = T[i]['message'].split()
#         start_index = T[i]['offset']
#         length = T[i]['length']
#         if 'spelling' in s:
#             spelling_mistakes += 1
#             l.append(essay[start_index:start_index+length])
#         else:
#             grammar_errors += 1
#         list_of_tuples.append((start_index,length))
#         list_of_errors.append((essay[start_index:start_index+length],T[i]['message'],T[i]['shortMessage'],T[i]['replacements'],T[i]['rule']))
#     features_dict['spelling_mistakes'] = spelling_mistakes
#     features_dict['grammar_errors'] = grammar_errors
#     features_dict['list_of_errors'] = ','.join(l)
#     features_dict['total_suggestions'] = list_of_errors
#     # features_dict['language_errors'] = language_errors
#     features_dict["word_count"] = word_count
#     features_dict["word_count_minus_stopwords"] = word_count_minus_stopwords
#     if word_count //  150:  # 150 word limit
#         features_dict["score"] = 10 - ((spelling_mistakes * 0.25) + (grammar_errors * 0.25) )
#         if features_dict["score"] < 0:
#             features_dict["score"]=0
#         # generate score with ml??
#     s = set(l)
#     essay2 = ""
#     for item in essay.split():
#         if item in s:
#             item = " <span class = 'report'>"+item+"</span> "
#         essay2 += item
#     features_dict['essay'] = essay2
#     return {"score": features_dict["score"], "grammar_errors": features_dict["grammar_errors"],
#             "spelling_mistakes": features_dict["spelling_mistakes"], "word_count":features_dict["word_count"],'list_of_errors': features_dict['list_of_errors'],'total_suggestions':features_dict['total_suggestions'],'essay':features_dict['essay']}









# # import nltk
# # from nltk.corpus import stopwords
# # import enchant
# # import re


# # def score_calculator(essay):
# #     features_dict = {"score": 0}
# #     d1 = enchant.Dict("en-US")
# #     d2 = enchant.Dict("en-GB")
# #     stop_words = set(stopwords.words('english'))

# #     # spelling mistakes, pos count, average sentence length, average word length, words greater than k characters
# #     # word count, word count excluding stop words, grammar mistakes
# #     spelling_mistakes = 0
# #     word_count_minus_stopwords = 0
# #     word_count = 0
# #     # cleaned_essay = re.sub(r"[.,?!;:]", "", essay)
# #     words = re.sub(r"[.,?!;:\"\']", " ", essay).split()

# #     for word in words:
# #         if d1.check(word) == False:
# #             if d2.check(word) == False:
# #                 print(word)
# #                 spelling_mistakes += 1
# #         else:
# #             pos = nltk.pos_tag([word])[0][1][:2]
# #             if pos not in features_dict:
# #                 features_dict[pos] = 1
# #             else:
# #                 features_dict[pos] += 18
# #             if word not in stop_words:
# #                 word_count_minus_stopwords += 1
# #         word_count += 1
# #     features_dict["spelling_mistakes"] = spelling_mistakes
# #     features_dict["word_count"] = word_count
# #     features_dict["word_count_minus_stopwords"] = word_count_minus_stopwords

# #     # grammar mistakes
# #     features_dict["grammar_errors"] = len(re.findall(r",[A-Za-z]", essay)) + len(
# #         re.findall(r"\.[A-Za-z]", essay)) + len(re.findall(r"\.[a-z]", essay)) + len(re.findall(r"\. [a-z]", essay))

# #     if word_count // 150:  # 150 word limit
# #         features_dict["score"] = 10 - ((spelling_mistakes * 0.5) + (features_dict["grammar_errors"] * 0.25))
# #         if features_dict["score"] < 0:
# #             features_dict["score"]=0
# #         # generate score with ml??

# #     return {"score": features_dict["score"], "grammar_errors": features_dict["grammar_errors"],
# #             "spelling_errors": features_dict["spelling_mistakes"], "word_count":features_dict["word_count"]}


