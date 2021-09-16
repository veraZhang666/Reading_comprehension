from flask import Flask, render_template, request, jsonify
import base64
import model
import json
import sys, os
import xunfeiAPI

current_directory = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.dirname(current_directory) + os.path.sep + ".")
sys.path.append(root_path)

app = Flask(__name__)

imgIdx = 0  # img accumulative filename img0.jpg,img1.jpg

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/uploadpic/', methods=['GET', 'POST'])
def uploadpic():
    if request.method == 'POST':  # and request.is_xhr
        img_str = request.form.get('pic')
        global imgIdx
        inx = img_str.find(',')
        newstring = img_str[inx + 1:]
        imgdata = base64.b64decode(newstring)
        picpath = 'uploads/image{}.jpg'.format(imgIdx)
        print('图片路径',picpath)
        imgIdx += 1

        # Save image to /uploads
        f = open(picpath, "wb")
        f.write(imgdata)
        f.close()
        # ------------TODO!!!------------
        # 拿到图片原文，问题，建议答案。高亮句子

        results = xunfeiAPI.getRecognitionResult(picpath)

        all_QA_list = model.get_all_QA(results)
        print(all_QA_list)
        # '<span class="highlight">'+searchtext+'</span>'
        idx_pair = []
        for dic in all_QA_list:
            start,end = dic['startidx'],dic['endidx']
            idx_pair.append((start,end))

        passage = model.get_passage(results)
        for dic in all_QA_list:
            dic['passage'] = passage
        li = all_QA_list

        print(li)
    return jsonify(li)



if __name__ == '__main__':
    print("test ok")
    app.run(port=5003)
