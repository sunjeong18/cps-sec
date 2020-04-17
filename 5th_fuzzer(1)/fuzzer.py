# -*- coding: utf-8 -*-

import random
import math
import os, sys
import threading
import glob
import time
#import utils
import shutil
from datetime import datetime
import gc
import subprocess
# for email
import smtplib
import signal


FUZZ_DELAY = 6
USE_WINDBG = False 
EXPLOITABLE_FRE = 6

# argv[1] exe파일target , argv[2] zip파일 ext

class File_Fuzzer:
    def __init__(self,target ,ext):
    
        self.base_path = os.getcwd() + "/" # 경로를 가져옴 
        self.target =target
        self.target_path = self.base_path + os.path.basename(target) + "/"
        self.sample_path = self.base_path + "samples/"
        self.test_path = self.target_path + "test/"
        self.crash_path = self.target_path +  "crash/"
        self.exploitable_path = self.target_path + "crash/exploitable/"
        self.sample_ext = ext
        self.sample_stream = None
        self.case_name = None
        self.crash_fname = ''
        self.iter = 0
        self.running = False
        self.crash_count = 0
        self.dbg = None
        self.mutate_method = ""
        self.mutate_byte = ""
        self.mutate_offset = 0
        self.mutate_len = 0
        self.orig_bytes = ""
        self.exploitable_count = 0
        self.exploitable_hashset = []
        self.title_exploitable_count = 0
        self.title_probably_exploitable_count = 0

        
        if not os.path.exists(self.target_path): 
            os.mkdir(self.target_path) #path에 디렉토리 존재하지 않는다면 만들어준다.
        if not os.path.exists(self.sample_path):
            os.mkdir(self.sample_path)
        if not os.path.exists(self.test_path):
            os.mkdir(self.test_path)
        if not os.path.exists(self.crash_path):
            os.mkdir(self.crash_path)
        if not os.path.exists(self.exploitable_path):
            os.mkdir(self.exploitable_path)
            
    def File_Picker(self):
        sample_list = glob.glob(self.sample_path + self.sample_ext + '/*') # 파일 목록 표시해주기 watch에서 sample_list검색하면 나옴 
        if len(sample_list) < 1:
            print (" [-] 샘플이 존재하지 않습니다. sample 폴더를 확인해 주세요.")
            sys.exit()
        while 1:
            sample = random.choice(sample_list) #sample파일 중 랜덤으로 하나 불러오기 
            self.sample_stream = open(sample,"rb").read() # sample파일을 byte단위로 읽어오기 read byte ->sample stream에 저장 
            #print(self.sample_stream[0:10])
            if len(self.sample_stream) > 1:
                break
        return

      # case 0 : 값을 랜덤하게 변경한다.
      # case 1 : 값을 랜덤하게 삽입한다.

    def Mutate(self):
        global mutated_stream 
        global mutate_byte
        test_cases = [ "\x00", "\xff", "\x41", "%%s"]# testcase에 리스트 담아두기 
        case = random.randint(0, 1) # case가 0 혹은 1일 경우 이것도 랜덤하게  
    # case = 1
    # mutate_count = int(random.randint(1, len(self.sample_stream)) * 0.005)+1 # 전체 변경 바이트 수
    # mutate_count = random.randint(1,2) #1과 2중에 얼마나 반복할건지 랜덤값을 뽑아서 mutate에 저장 
    # test_cases.append(str(random.randint(0,255)))
        mutate_byte = random.choice(test_cases)#testcase 4개 중에서 랜덤하게 하나 선택해서 저장되어있고  그 바이트로 변경 혹은 삽입  
        self.mutate_byte = mutate_byte
        if case == 0:   # replace
            print (" [+] Case 1. Byte Replace  ")
            self.mutate_case = 0
            for i in range(mutate_count):
                mutate_offset = random.randint(1, len(self.sample_stream)) # 변경 offset : 떨어진 정도 
                #sample stream에는 byte단위로 불러온 것들이 있다. 1부터 전체 byte길이 중에 랜덤값 선택해서 offset에 저장
                mutate_len = random.randint(1,500)   # 변경 바이트 길이
                # \x00", "\xff", "\x41", "%%s 이 중에서 replace가 될텐데 어디부터 어디까지 변경 replace할건지 랜덤하게 뽑음 
                mutated_stream = self.sample_stream[0:mutate_offset] # 0번부터 mutate_offset까지 자르기 
                
                temp = [] #  byte 연산 
                for i in range (mutate_len): #ex. 282
                    temp.append(self.mutate_byte) #temp라는 리스트에다가 ex. %%s append추가하기
                print(temp)
                temp = "".join(temp)# 리스트에 있는걸 string 으로 변환해주기 
                print(temp)
                ms = bytearray(mutated_stream) #byte형식으로 바꿔줘서 
                ms += temp.encode() # temp에 %%s 282개 있는걸 byte형태로 encode해줘서 ms에 저장 
                print(ms[-10:]) # 282 개중 마지막 뒤에 10개만 
                ms += self.sample_stream[mutate_offset + mutate_len:] #len : 282 
                # print(ms[-10:])
                print (" [+] replace %d bytes" % (mutate_len)) # 얼마만큼의 byte가 바뀌었나

        else:         # add
            print (" [+] Case 2. Byte Insertion ")
            self.mutate_case = 1
            mutate_offset = random.randint(1, len(self.sample_stream)) # 변경 offset 
            mutate_len = random.randint(1,30000)   # 변경 바이트 길이
            mutated_stream = self.sample_stream[0:mutate_offset]
            
            #print (mutated_stream)
            #mutated_stream += mutate_byte * mutate_len
            temp = []
            for i in range (mutate_len):
                temp.append(self.mutate_byte)
            print(temp)
            temp = "".join(temp)
            print(temp)
            ms = bytearray(mutated_stream)
            ms += temp.encode()
            print(ms[-10:])
            ms += self.sample_stream[mutate_offset:] # len뒤에 붙어버리기 때문에 
            print ("  [+] Mutated %d bytes(add)" % (mutate_len) )

        self.mutate_offset = mutate_offset
        self.case_name = self.test_path + "case-%s.%s" % (str(self.iter),self.sample_ext)
        f = open(self.case_name ,"wb")
        f.write(bytes(ms))
        f.close()  # sample에 replace해서 파일 써주기  
        return 

    def Fuzzing(self, count):
        self.count = count
        print (self.count)
        self.File_Picker()
        self.Mutate()

if __name__ == '__main__':
    print ("Usage example : C:/Users/chj09/Desktop/fuzzer/reader.exe, zip ")

    if len(sys.argv) !=3:
        print ("[SYSTEM] Error .... Please Chqeck Usage")
        sys.exit()

    print ("[SYSTEM] Fuzzer Start ")

    fuzzer = File_Fuzzer(sys.argv[1], sys.argv[2])
    fuzzer.Fuzzing(5000)