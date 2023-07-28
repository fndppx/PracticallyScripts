import os
import matplotlib.pyplot as plt
import numpy as np
import PIL
from PIL import Image
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
print(tf.__version__);
#print(tf.keras.__version__);



def classify_image_saved_model(model_path, predicted_image_path, labels_path):
        
    # 加载SavedModel
    loaded_model = tf.saved_model.load(model_path)

    # 读取和预处理图像
    image_path = predicted_image_path

    with open(labels_path, 'r') as f:
        labels = f.read().splitlines()
        
    # 获取签名函数
    infer = loaded_model.signatures['serving_default']
    #print("11",list(loaded_model.signatures.values))
#    print("打印签名>>>>>>>",loaded_model.signatures['serving_default'])

    # 读取和预处理图像
    #image_path = '/path/to/image.jpg'
    image = Image.open(image_path).resize((224, 224))  # 调整图像大小
    image = np.array(image)  # 将图像转换为NumPy数组
    image = image / 255.0  # 归一化图像
    image = image.astype(np.float32)  # 将数据类型转换为float32
    image = np.expand_dims(image, axis=0)  # 添加批次维度

    # 调用签名函数进行推断
    output = infer(inputs=tf.constant(image))
    #print("11",output)
    #print(loaded_model.signatures['serving_default'])

    # 获取输出结果
    output_data = output['logits'].numpy()

    # 根据模型输出获取分类结果
    class_index = np.argmax(output_data)
    confidence = output_data[0][class_index]
    predicted_label = labels[class_index]

    # 输出预测结果
    print('预测类别：', predicted_label)
    print('预测准确度：', confidence * 0.1)

def classify_image_tflite(model_path, predicted_image_path, labels_path):

    # 加载TFLite模型 converted_model_0705.tflite   origin_model convert_origin_model.tflite  origin_mobilenet_v3_large_100_224.tflite
    TF_MODEL_FILE_PATH = model_path
    interpreter = tf.lite.Interpreter(model_path=TF_MODEL_FILE_PATH)
    interpreter.allocate_tensors()
#    print('打印签名>>>>>>>',interpreter.get_signature_list())

    signature_runner = interpreter.get_signature_runner('serving_default')

    # 加载标签文件
    with open(labels_path, 'r') as f:
        labels = f.read().splitlines()

    # 读取和预处理图像
    image_path = predicted_image_path
    image = Image.open(image_path).resize((224, 224))  # 调整图像大小
    image = np.array(image)  # 将图像转换为NumPy数组
    image = image / 255.0  # 归一化图像
    image = np.expand_dims(image, axis=0).astype(np.float32)  # 添加批次维度并转换为float32

    # 设置模型输入和输出张量
    input_tensor_index = interpreter.get_input_details()[0]['index']
    output_tensor_index = interpreter.get_output_details()[0]['index']

    # 设置输入张量的值
    interpreter.set_tensor(input_tensor_index, image)

    predictions_lite = signature_runner(inputs=image)['logits']
    score_lite = tf.nn.softmax(predictions_lite)

    # 获取预测类别索引
    class_index = np.argmax(score_lite)
    predicted_label = labels[class_index]
    confidence = score_lite[0][class_index]

    # 输出预测结果
    print('预测类别：', predicted_label)
    print('预测准确度：', confidence)


def classify_image_tflite_no_sin(model_path, predicted_image_path, labels_path):


    TF_MODEL_FILE_PATH = model_path
    interpreter = tf.lite.Interpreter(model_path=TF_MODEL_FILE_PATH)
    interpreter.allocate_tensors()
    
    # 加载标签文件
    with open(labels_path, 'r') as f:
        labels = f.read().splitlines()

    # 读取和预处理图像
    image_path = predicted_image_path
    image = Image.open(image_path).resize((224, 224))  # 调整图像大小
    image = np.array(image)  # 将图像转换为NumPy数组
    image = image / 255.0  # 归一化图像
    image = np.expand_dims(image, axis=0).astype(np.float32)  # 添加批次维度并转换为float32

    # 设置模型输入和输出张量
    input_tensor_index = interpreter.get_input_details()[0]['index']
    output_tensor_index = interpreter.get_output_details()[0]['index']

    # 设置输入张量的值
    interpreter.set_tensor(input_tensor_index, image)

    # 执行推断
    interpreter.invoke()

    # 获取输出张量的结果
    output_data = interpreter.get_tensor(output_tensor_index)
    
    score_lite = tf.nn.softmax(output_data)

    # 获取预测类别索引
    class_index = np.argmax(score_lite)
    predicted_label = labels[class_index]
    confidence = score_lite[0][class_index]

    # 输出预测结果
    print('预测类别：', predicted_label)
    print('预测准确度：', confidence)
    

labels_path = '/Users/dxm/Desktop/测试数据源/labels.txt'

#print('tf未转换的savedmodel模型')
#for i in range(1,18):
#    model_path = '/Users/dxm/Desktop/测试数据源/原始tf模型/imagenet_mobilenet_v3_large_100_224_classification_5'
#    predicted_image_path = '/Users/dxm/Desktop/TensorflowTest/TensorflowTest/ImageRes/tensor_%s.jpg'%(str(i))
#
#    #savedmodel
#    classify_image_saved_model(model_path, predicted_image_path, labels_path)
#
#print('转换后不带标签的tflite模型')
#for i in range(1,18):
#    #转换后不带标签的模型
#    model_path = '/Users/dxm/Desktop/测试数据源/转换后不带标签的tf模型/converted_model.tflite'
#    predicted_image_path = '/Users/dxm/Desktop/TensorflowTest/TensorflowTest/ImageRes/tensor_%s.jpg'%(str(i))
#
#    classify_image_tflite(model_path, predicted_image_path, labels_path)


print('转换后带标签的tflite模型')
for i in range(1,18):
    #转换后带标签的tf模型
    model_path = '/Users/dxm/Desktop/测试数据源/转换后带标签的tf模型/converted_model.tflite'
    predicted_image_path = '/Users/dxm/Desktop/TensorflowTest/TensorflowTest/ImageRes/tensor_%s.jpg'%(str(i))

    classify_image_tflite_no_sin(model_path, predicted_image_path, labels_path)
    
#print('原始带标签的tflite模型')
#for i in range(1,18):
#    #原始带标签的tf模型
#    model_path = '/Users/dxm/Desktop/测试数据源/origin_has_labels_model.tflite'
#    predicted_image_path = '/Users/dxm/Desktop/TensorflowTest/TensorflowTest/ImageRes/tensor_%s.jpg'%(str(i))
#
#    classify_image_tflite_no_sin(model_path, predicted_image_path, labels_path)
