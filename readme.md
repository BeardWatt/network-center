# 说明

[TOC]

<img src="readme.assets/install2macOS.png" alt="install2macOS" style="zoom:30%;" />

## 功能

自动根据照片的EXIF信息，在照片文件名后添加拍摄日期（月、日）和时间（时、分）

## 运行方式

运行可执行文件，或

```bash
# 源码运行
python3 main.py
```

## 运行效果截图

### macOS

![ExifPic@macOS](readme.assets/ExifPic@macOS.jpg)

### Windows 10

![ExifPic@win10](readme.assets/ExifPic@win10.PNG)

### Windows 7

![ExifPic@win7](readme.assets/ExifPic@win7.PNG)

## 依赖

见requirements.txt

## 手机发送照片到电脑

**重命名必须依赖EXIF信息**

- 安卓：使用手机相机拍摄的照片，可以使用微信，发送原图到电脑。**不能**直接用微信拍照发送，会丢失EXIF信息。
- iPhone：iPhone 7之后的机型，默认照片格式为HEIC，通过微信发送到电脑会丢失EXIF信息，有条件可以使用Airdrop，或使用如下解决方法。
  1. 在iPhone手机上：设置 - 相机 - 格式 - 兼容性最佳，使照片默认使用JPEG格式，规避微信发送时的格式转换
  2. 相机拍摄照片，然后使用微信发送原图

## 已知缺漏及解决方法

- Mac端ExifPic.app第一次运行会疑似闪退，无需任何操作，会自动重新启动
- Windows端第一次启动需要较长时间，无需任何操作，稍等片刻即可
- 在Windows 7上，可能会报错`api-ms-win-crt-process-l1-1-0.dll 丢失`，参考[这个](https://blog.csdn.net/gangeqian2/article/details/79307416)网站
  1. 打开Windows Update服务
  2. 安装[KB2999226](https://support.microsoft.com/en-us/help/2999226/update-for-universal-c-runtime-in-windows)、[KB3118401](https://support.microsoft.com/en-us/help/3118401/update-for-universal-c-runtime-in-windows)两个补丁

## 反馈邮箱

beardwatt@gmail.com