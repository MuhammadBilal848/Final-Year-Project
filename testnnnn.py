# def calculate_overall_performance(accuracy_scores):
#     total_weight = len(accuracy_scores) * 10  # Each question has a weight of 10
    
#     weighted_sum = sum(accuracy * 10 for accuracy in accuracy_scores)
    
#     overall_performance = weighted_sum / total_weight
#     return overall_performance

# # Example accuracy scores for 10 answers (ranging from 0 to 100)
# accuracy_scores = [80, 90, 70, 85, 95, 60, 75, 88, 78, 92]

# result = calculate_overall_performance(accuracy_scores)
# print("Overall Performance:", result)


# def clean_and_convert_percentage_strings(percentage_strings):
#     cleaned_integers = []
#     for string in percentage_strings:
#         cleaned_string = string.strip('%')  
#         integer_value = int(cleaned_string)  
#         cleaned_integers.append(integer_value)
#     return cleaned_integers

# percentage_strings = [
#   "6000%",
#   "40%",
#   "10%",
#   "90%"
# ]


# cleaned_integers = clean_and_convert_percentage_strings(percentage_strings)
# print(cleaned_integers)

# print(calculate_overall_performance(clean_and_convert_percentage_strings(['20%','30%','10%','56%','89%','34%','80%'])))


