import matplotlib

matplotlib.use('Agg')
import os

import time
import paddlex as pdx

os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['CPU_NUM'] = '16'

print('-----加载模型-----')

paddlex_model_src = "model/home/aistudio/output/face/faster_rcnn_r50_fpn/epoch_2"
from paddlex.det import transforms

eval_transforms = transforms.Compose([
    transforms.ResizeByShort(short_size=800, max_size=1333),
    transforms.Padding(coarsest_stride=32)
])
model = pdx.load_model(paddlex_model_src)

a = time.time()
result = model.predict("visualize_1621402647709.jpg", eval_transforms)
print(result)
# pdx.det.visualize(img, result, threshold=0.7, save_dir='./')
menu = []
for item in result:
    if (item["score"] > 0.8):
        menu.append(item["category"])
b = (time.time() - a)
print(b)
