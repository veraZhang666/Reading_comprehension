import torch
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
from utils import *

# ==========call method in utils ===============

model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')




# Apply the tokenizer to the input text, treating them as a text-pair.


# Search the input_ids for the first instance of the `[SEP]` token.

# print('shapeof input_ids', len(input_ids))

# Run our example through the model.
def get_input_ids_segment_ids(answer_text,total_qes_ans_list):
    input_ids_list = []
    segment_ids_list = []
    for qs in total_qes_ans_list:
        question = qs[0] # get the question sentence
        input_ids = tokenizer.encode(question, answer_text)
        input_ids_list.append(input_ids)

        sep_index = input_ids.index(tokenizer.sep_token_id)
        # The number of segment A tokens includes the [SEP] token istelf.
        num_seg_a = sep_index + 1
        # The remainder are segment B.
        num_seg_b = len(input_ids) - num_seg_a

        # Construct the list of 0s and 1s.
        segment_ids = [0] * num_seg_a + [1] * num_seg_b
        # There should be a segment_id for every input token.
        assert len(segment_ids) == len(input_ids)
        segment_ids_list.append(segment_ids)
    return input_ids_list,segment_ids_list
    # predict

def get_all_QA(result):
    page, num_choices = get_page_text(result)
    passage, question_answers = get_passage_from_page(page, num_choices)
    total_qes_ans_list = get_questions_answers(question_answers, num_choices)

    answer_text = passage
    all_QA_list = []

    input_ids_list,segment_ids_list =  get_input_ids_segment_ids(answer_text,total_qes_ans_list)
    num_questions = len(total_qes_ans_list)

    for i in range(num_questions):
        input_ids = input_ids_list[i]
        segment_ids = segment_ids_list[i]
        tokens = tokenizer.convert_ids_to_tokens(input_ids)
        outputs = model(torch.tensor([input_ids]), # The tokens representing our input text.
                                 token_type_ids=torch.tensor([segment_ids]), # The segment IDs to differentiate question from answer_text
                                 return_dict=True)
        start_scores = outputs.start_logits
        end_scores = outputs.end_logits
        # Find the tokens with the highest `start` and `end` scores.
        answer_start = torch.argmax(start_scores)
        answer_end = torch.argmax(end_scores)

        # Combine the tokens in the answer and print it out.
        answer = ' '.join(tokens[answer_start:answer_end + 1])

        # 3 all string
        answer_Dict = getanserDict(answer,total_qes_ans_list[i][1])
        answer_Dict['startidx'] = answer_start.item()
        answer_Dict['endidx'] = answer_end.item()
        answer_Dict['question'] = total_qes_ans_list[i][0]
        all_QA_list.append(answer_Dict)

    return all_QA_list
def get_passage(result):
        page, num_choices = get_page_text(result)
        passage, _ = get_passage_from_page(page, num_choices)
        return passage

# ======================GET ANSWER==============
def getanserDict(answer,options):
    from sklearn.metrics.pairwise import cosine_similarity
    from sentence_transformers  import SentenceTransformer
    import numpy as np

    sentence2OP = {}
    for v,k in options.items():
      sentence2OP[k]=v
    sentences = [answer]
    for s in list(options.values()):
      sentences.append(s)
    model_name = 'bert-base-nli-mean-tokens'

    model = SentenceTransformer(model_name)

    msentence_vec = model.encode(sentences)

    ans_prob = cosine_similarity([msentence_vec[0]], msentence_vec[1:])
    all_option ='所有答案选项为: '+ str(options)
    hint = '答案提示: ' + answer
    correct_idx = np.argmax(ans_prob)
    key = sentences[correct_idx + 1]
    predict = '预测正确答案选项为:' + sentence2OP[key]

    answer_Dict = {}
    answer_Dict['opts'] = all_option
    answer_Dict['highlight'] = hint
    answer_Dict['pred'] = predict
    return answer_Dict



if __name__ == '__main__':
    pass
    #print(get_all_QA(answer_text, total_qes_ans_list))