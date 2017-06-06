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
