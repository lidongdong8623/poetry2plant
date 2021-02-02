# -*- coding: utf-8 -*-
import speech_recognition as sr
import  cv2
import numpy as np
from poetry import poetry
def Poetry2PlantImage(text):
	path = []
	for t in text:
		if t in poetry.keys():
			path += poetry[t]

	return ConcateImage(path)

def ConcateImage(image_path:list):
	if len(image_path) == 0:
		return None
	plant_image = []
	# 所有图片读出，添加到list
	for path in image_path:
		path = 'plant/img/' + path
		img = cv2.imread(path)
		plant_image.append(img)
	if len(plant_image) > 0:
		if len(plant_image) == 1:
			show_image = plant_image[0]
		else:
			plant_image = [cv2.resize(i, (0,0), fx=0.5, fy=1) for i in plant_image]
			if len(plant_image) == 2:
				show_image = np.concatenate(plant_image,axis=1)
			elif len(plant_image) == 3:
				blank_image = np.ones_like(plant_image[2])*255
				row_0 = np.concatenate(plant_image[:2], axis=1)
				row_0 = cv2.resize(row_0, (0,0), fx=1, fy=0.5)
				row_1 = np.concatenate([plant_image[2], blank_image], axis=1)
				h,w,_ = row_0.shape
				row_1 = cv2.resize(row_1, (w, h))
				show_image = np.concatenate([row_0, row_1], axis=0)
			elif len(plant_image) == 4:
				row_0 = np.concatenate(plant_image[0:2], axis=1)
				row_1 = np.concatenate(plant_image[2:4], axis=1)
				row_0 = cv2.resize(row_0, (0,0), fx=1, fy=0.5)
				h,w,_ = row_0.shape
				row_1 = cv2.resize(row_1, (w, h))
				show_image = np.concatenate([row_0, row_1], axis=0)
			else:
				show_image = None
	else:
		show_image = None
	return show_image

if __name__ == "__main__":
	# obtain audio from the microphone
	r = sr.Recognizer()
	continue_image = cv2.imread('plant/continue.jpg')
	sorry_image = cv2.imread('plant/sorry.jpg')
	tips_image = cv2.imread('plant/tips.jpg')
	#tips_image = cv2.resize(tips_image,(0,0),fx=0.5, fy=0.5)
	recognizing_image = cv2.imread('plant/recognizing.jpg')
	cv2.namedWindow('poetry2image', cv2.WINDOW_NORMAL)
	cv2.setWindowProperty('poetry2image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
	while True:
		with sr.Microphone() as source:
			r.adjust_for_ambient_noise(source)  # listen for 1 second to calibrate the energy threshold for ambient noise levels
			# 显示一张“请说一句古诗”图片
			text = 'Go!'
			org = (40, 80)
			fontFace = cv2.FONT_HERSHEY_COMPLEX
			fontScale = 1.3
			fontcolor = (255, 255, 255) # BGR
			thickness = 3
			lineType = 4
			bottomLeftOrigin = 1
			cv2.putText(continue_image, text, org, fontFace, fontScale, fontcolor, thickness, lineType)
			cv2.imshow('poetry2image', continue_image)
			cv2.waitKey(1)
			# print("")
			audio = r.listen(source)
			cv2.imshow('poetry2image', recognizing_image)
			cv2.waitKey(1)
		#
		# # recognize speech using Sphinx
		text = ''
		try:
			text = r.recognize_sphinx(audio, language="zh-CN")
			print("Sphinx thinks you said: " + text)
		except sr.UnknownValueError:
			print("Sphinx could not understand audio")
		except sr.RequestError as e:
			print("Sphinx error; {0}".format(e))
		# 针对一次说两句的情况
		text = text.split(' ')
		if '' in text:
			text.remove('')
		#print("按‘q’键退出,按任意键继续……")
		show_image = sorry_image
		if len(text) > 0:
			plant_image = Poetry2PlantImage(text)
			if plant_image is not None:
				show_image = plant_image
			else:
				print("Warning:sphinx thinks you said：{},but can not find corresponding image".format(text))
		h , w, _ = tips_image.shape
		show_image = cv2.resize(show_image, (1024,768))
		#show_image[0:h, 0:w,:] = tips_image

		text = '5'
		org = (40, 80)
		fontFace = cv2.FONT_HERSHEY_COMPLEX
		fontScale = 1.3
		fontcolor = (255, 255, 255) # BGR
		thickness = 3
		lineType = 4
		bottomLeftOrigin = 1
		cv2.putText(show_image, text, org, fontFace, fontScale, fontcolor, thickness, lineType)
		cv2.imshow('poetry2image', show_image)
		cv2.waitKey(1000)
		text = '4'
		org = (70, 80)
		cv2.putText(show_image, text, org, fontFace, fontScale, fontcolor, thickness, lineType)
		cv2.imshow('poetry2image', show_image)
		cv2.waitKey(1000)
		text = '3'
		org = (100, 80)
		cv2.putText(show_image, text, org, fontFace, fontScale, fontcolor, thickness, lineType)
		cv2.imshow('poetry2image', show_image)
		cv2.waitKey(1000)
		text = '2'
		org = (130, 80)
		cv2.putText(show_image, text, org, fontFace, fontScale, fontcolor, thickness, lineType)
		cv2.imshow('poetry2image', show_image)
		cv2.waitKey(1000)
		text = '1'
		org = (160, 80)
		cv2.putText(show_image, text, org, fontFace, fontScale, fontcolor, thickness, lineType)
		cv2.imshow('poetry2image', show_image)
		cv2.waitKey(1000)
		text = 'Ready?'
		org = (190, 80)
		cv2.putText(show_image, text, org, fontFace, fontScale, fontcolor, thickness, lineType)
		cv2.imshow('poetry2image', show_image)
		cv2.waitKey(1)

	cv2.destroyAllWindows()