# CaffeServer
Flask backend for caffe image classification project

## How it works
This backend server receive client upload image, then call pycaffe script to classify image, return objects detected and its property.
response struct:
```
{
    "objects":
    [{
        "obj": Array[4],
        "class": String,
        "score": Number
    },
    {}
    ]
}
```
### 基于flask提供图像分类服务

根据[上一篇文章](http://www.jianshu.com/p/a83668dc4ad2)在云服务上搭建的pycaffe运行环境，为了使得这个机器学习环境能更友好地跑起来， 准备简单做一个后端服务，搭配几个简单的API，让用户可以通过网络请求来调取服务。特此开一个Github项目，记录下，后面还要做安卓平台的图像分类应用。
[CaffeServer 项目地址](https://github.com/alex2wong/CaffeServer)
该项目的依赖自然是pycaffe的运行环境，并且caffemodel在指定的磁盘位置。POST 请求 http://yourhost:8000/upload 端口，并且在body里带上包含图片文件的FormData，经过服务器的识别就可以返回JSON格式的识别结果：
```
{
    "objects":
    [{
        "obj": Array[4],  //识别出对象的外包矩形
        "class": String,  //标签名称，car，horse，bird ....
        "score": Number  //识别结果的confidence
    },{}]
}
```

【更新 2017/8/2】
提供了基于Angular4.x 构建的UI，来测试后端的CaffeServer 对象检测功能，在线[体验地址](http://111.231.11.20:3000/ngx-proj/dist/)，后端返回JSON 格式的识别结果

### 题外话，评价pix2code

![pix2code 图示，https://uizard.io/index.html#tech](http://upload-images.jianshu.io/upload_images/1950967-6245a3d3e935a002.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

针对最近比较火爆的pix2code 项目，[github地址](https://github.com/tonybeltramelli/pix2code). 可以根据Sketch或者PS的UI图直接生成UI代码，其中涉及到对DOM元素的识别和HTML代码，CSS的生成。虽然把机器学习用于代码生成看起来很高大上，不少人说AI太强了，程序猿是不是要失业了。在我看来，**不必惊慌**。就原作者的意思，这个只是个实验项目，并不成熟，目前只能做一些基础工作，用于减少工程师对UI代码的编写工作，更集中于业务的开发。

而且AI项目最大的问题就是，只是生成**静态代码**，也就是View层面的代码，而Controller，Model这些最关键的部分还是得靠有经验的程序猿根据业务需求去完成，调试，并且慢慢优化。AI 短时间内还很难帮助优化网络请求，界面渲染等问题。

阿里之前出了深度学习设计AI**鲁班**，也是同样道理，通过深度学习设计风格，产出设计图示，可以解决设计师的重复劳动，但这些有意思的设计风格也需要优秀的设计师花心思构思。AI 生产的图纸也需要设计师去修订，有的时候修订还不如推翻重来呢。。

以下链接中有 Vue作者尤雨溪的回答，比较客观，仔细想来AI要替代前端工程师的路还远。
[知乎：如何评价“代码直出工具”pix2code](https://www.zhihu.com/question/60352831/answer/175185625)
