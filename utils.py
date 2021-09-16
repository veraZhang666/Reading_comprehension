from xunfeiAPI import getRecognitionResult



def get_page_text(result):
    dic= eval(result)
    dic.keys()
    token_lists = dic['data']['block'][0]['line']
    page = ''
    sentence_list = dic['data']['block'][0]['line'][10]['word']
    for tok_list in token_lists:
        for d in tok_list['word']: # [{'content': 'same'}, {'content': 'student'}
            page+= ''.join(d['content'])+' '
    for st in range(1,11):
        old = str(st)+' .'
        new = str(st)+'.'
        page=page.replace(old,new)
    news = ['A.','B.','C.','D.']
    i = 0
    for st in ['A .','B .','C .','D .']:
        page = page.replace(st,news[i])
        i+=1
    page = page.replace('_','')
    num_choices = 4
    if page.find('D.') == -1:
        num_choices =  3
    return page,num_choices


import collections


def get_passage_from_page(page, num_choices):
    passage = None
    orders = ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.']
    idx = [page.find(order) for order in orders]
    l = [i for i in idx if i != -1]  # [468, 536]
    l.append(len(page))
    question_answers = []
    if len(l) != 0:
        passage = page[0:l[0]]
        for i in range(len(l) - 1):
            sent = page[l[i]:l[i + 1]]
            question_answers.append(sent)
    else:
        print('找不到问题~')
    return (passage, question_answers)


# 拿到每个问题的答案，并把ABCD/ABC答案做成键值对
def get_questions_answers(question_answers, num_choices):
    total_qes_ans = []
    for i in range(len(question_answers)):
        # get_ques_ans(question_answers[i], num_choices)
        l = get_ques_ans(question_answers[i], num_choices)
        if l == None:
            print('no questions or answers provied')
            return None
        total_qes_ans.append(l)
    return total_qes_ans


# return ['single question',{'A:':'xxx','B':xxx}]
def get_ques_ans(question, num_choices):
    abcd_dict = {}
    res = question.split('A.')
    ques = res[0]
    ans_all = res[1]
    a_res = ans_all.split('B.')
    abcd_dict['A'] = a_res[0]
    ans_all = a_res[1]

    b_res = ans_all.split('C.')

    abcd_dict['B'] = b_res[0]
    ans_all = b_res[1]

    c_res = ans_all.split('D.')
    abcd_dict['C'] = c_res[0]
    if num_choices == 3:
        l = [ques, abcd_dict]
        return l
    d_res = c_res[1]
    abcd_dict['D'] = c_res[1]
    l = [ques, abcd_dict]
    print(abcd_dict)

    return l



if __name__ == '__main__':
    pass

