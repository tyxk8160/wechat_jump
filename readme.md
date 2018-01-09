# 微信跳一跳脚本
## 基本思路
 通过adb shell获取截屏图像，之后采用opencv识别出小跳棋和下一个物体的中心

---
## 具体实现
* 截屏
```sh
adb shell scenncap -p /sdcard/autojump.png
adb pull /sdcard/autojump.png  .
```
* 模拟触屏操作
```sh
adb shell input swipe x y x y time(ms)
```
模拟触屏的操作也比较简单（当然这部分是抄袭的）

* 小跳棋的识别
因为小跳棋形状和位置都没有改变过，所以我直接采用模板匹配的方法去识别小跳棋，实践证明，识别准确率超级高
```python
method  = cv2.TM_CCOEFF
res = cv2.matchTemplate(test_imge, chess_imge, method)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)
cv2.rectangle(test_imge,top_left,bottom_right,(255,0,255),2)
cv2.imwrite("detect_chess.png",test_imge)
plt.imshow(test_imge)
plt.show()
```
<img src = "https://github.com/tyxk8160/wechat_jump/raw/master/chess.png">
<img src = "https://github.com/tyxk8160/wechat_jump/raw/master/img/detect_chess.png">

* 下一个物体中心的识别
识别思路很简单：直接将图片进行边缘检测，边缘检测后得到二值图片。考虑到这些物体的中心大多是最长一行的中点，所以我直接寻找最长的一行，并求出它的中心，把这当物体中心。
边缘检测代码：
```python
edges = cv2.Canny(image,50,150)
```
<img src="https://github.com/tyxk8160/wechat_jump/raw/master/img/cany_sample.png">
从结果上看,canny检测效果不错，不过那小人似乎对最长的一行检测有干扰。由于模板匹配可以得到小人的精确位置，所以再做边缘检测后，我直接将小人的那一部分区域标记为黑色，这样就不影响结果了。
物体中心识别，直接贴图：

---
<img src="https://github.com/tyxk8160/wechat_jump/raw/master/detect/dect_0.png">
<img src="https://github.com/tyxk8160/wechat_jump/raw/master/detect/dect_40.png">
总体上看，识别效果还不错

# 安装
* adb 驱动和adb tools
* python
* opencv-python and matplotlib