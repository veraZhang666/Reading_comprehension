# Reading_comprehension



这是一个初中阅读题目解析的小项目：

  input:
  接受图片jpg/png/图片， 识别三个选项和四个选项的单选题。
  目前仅支持上传问题题号从1开始的英语阅读题目，而且是单选题，bug修复好了我再更新...

  output:
  1.答案对应的英文句子，单词在文章中的位置
  2.答案选项（ABCD、ABC）之一

    这个项目图片识别部分用的是科大讯飞的服务。

    需要自己去科大讯飞官网申请打印图片识别成文字的应用，然后填入自己的应用APPID, API_KEY
    在 xunfeiAPI.py中, 请替换自己的 ID 和 KEY
    https://doc.xfyun.cn/rest_api/%E5%8D%B0%E5%88%B7%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB.html
    # 应用ID (必须为webapi类型应用，并印刷文字识别服务，参考帖子如何创建一个webapi应用：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=36481)
    APPID = "XXXX"
    # 接口密钥(webapi类型应用开通印刷文字识别服务后，控制台--我的应用---印刷文字识别---服务的apikey)
    API_KEY = "XXXXX"


    视频讲解地址： https://www.bilibili.com/video/BV1hf4y1w792/
    视频colab: https://colab.research.google.com/drive/1X7xz1UE50IPGmoKkL4WdtYiejMiva9Iw?usp=sharing
    author: vera
    email: verazhang3333@gmail.com

    采用技术： flask + pytorch + transformer + jquery





![Image text](https://github.com/veraZhang666/Reading_comprehension/blob/master/process_structure.png?raw=true)
![Image text](https://github.com/veraZhang666/Reading_comprehension/blob/master/pageScreenshotpng.png?raw=true)
