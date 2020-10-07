#-*- coding: utf-8 -*-

# 필요한 라이브러리를 불러옵니다.

import spidev
import time
import RPi.GPIO as GPIO

#pin number 설정
blue_pin = 14
yellow_pin = 15
red_pin = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# LED 핀의 OUT설정
GPIO.setup(blue_pin, GPIO.OUT)
GPIO.setup(yellow_pin, GPIO.OUT)
GPIO.setup(red_pin, GPIO.OUT)

# 딜레이 시간 (센서 측정 간격)
delay = 0.5

# MCP3008 채널중 센서에 연결한 채널 설정
ldr_channel = 0

# SPI 인스턴스 spi 생성
spi = spidev.SpiDev()

# SPI 통신 시작하기
spi.open(0, 0)

# SPI 통신 속도 설정
spi.max_speed_hz = 100000

# 0 ~ 7 까지 8개의 채널에서 SPI 데이터를 읽어옵니다.
def readadc(adcnum):
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data

#readadc(adcnum)에서 받아온 광도의 결과값을 변수로 하여 전구 색상을 변경
def led_color(ldr_value):
    if ldr_value<=300:
        GPIO.output(blue_pin,1)
        print("blue")
        GPIO.output(yellow_pin,0)
        GPIO.output(red_pin,0)
          
    elif 300<ldr_value<500:
        GPIO.output(yellow_pin,1) 
        print("yellow")
        GPIO.output(blue_pin,0)
        GPIO.output(red_pin,0)
        
    elif 700<=ldr_value:
        GPIO.output(red_pin,1)
        print("red")
        GPIO.output(blue_pin,0)
        GPIO.output(yellow_pin,0)

while True:
 # readadc 함수로 ldr_channel의 SPI 데이터를 읽어옵니다.// led_color 함수를 readadc함수와 함께 반복
  ldr_value = readadc(ldr_channel)
  print ("---------------------------------------")
  print("LDR Value: %d" % ldr_value)
  led_color(ldr_value)
  time.sleep(delay)