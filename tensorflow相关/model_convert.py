import tensorflow as tf
import os
print(tf.__version__)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "1"
os.environ["MLIR_CRASH_REPRODUCER_DIRECTORY"] = ""
  

# 加载 SavedModel
saved_model_dir = "/Users/dxm/Desktop/测试数据源/原始tf模型/imagenet_mobilenet_v3_large_100_224_classification_5"

# Convert the model
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir) # path to the SavedModel directory
tflite_model = converter.convert()

# Save the model.
with open('converted_model.tflite', 'wb') as f:
  f.write(tflite_model)

