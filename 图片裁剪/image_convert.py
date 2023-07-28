
from PIL import Image
import os

def resize_images(input_folder, output_folder, width):
    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
            # 打开图像文件
            image_path = os.path.join(input_folder, filename)
            image = Image.open(image_path)
            
            # 调整图像大小
            resized_image = image.resize((width, int(width * image.size[1] / image.size[0])))
            
            # 保存调整大小后的图像
            output_path = os.path.join(output_folder, filename)
            resized_image.save(output_path)
            
            print(f"Resized {filename} successfully!")
# 输入文件夹路径，包含要调整大小的图片
input_folder = "/Users/dxm/Desktop/未命名文件夹/image"

# 输出文件夹路径，调整大小后的图片将保存在这里
output_folder = "/Users/dxm/Desktop/未命名文件夹/image/out"

# 要设置的目标宽度和高度
target_width = 200
#target_height = 200

# 调用函数进行批量调整大小
resize_images(input_folder, output_folder, target_width)
