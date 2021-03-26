import os
import librosa
import numpy as np
from scipy.io import wavfile


# out
dir_p = 'splited_wavs'


def time2seconds(s):
    print('ssssss:', s)
    # '0:00:11.203'
    a = s.split(':')
    print('aaaa:', a[0])
    h = float(a[0])
    m = float(a[1])
    s = float(a[2])

    res = h * 3600 + m * 60 + s
    return res



def write_wav(write_path, wav_arr, sr):
    wav_arr *= 32767 / max(0.01, np.max(np.abs(wav_arr)))
    wavfile.write(write_path, sr, wav_arr.astype(np.int16))
    return



def getRight(times_a, t):
    print('times_a:', times_a.shape)
    res = 0
    for i in range(times_a.shape[0]):
        if times_a[i] > t:
            break
        res = i
    print('res:', res)
    return res
    




class Speech(object):
    # ['0020001', 'huya_zdx_103.16k', '二号超粉日嘛就10899嘛，后来，后来偷懒嘛就把前面那个10给去了，去了后面那个688就没改了，就变成10，就变成899了。', '0:00:00.000', '0:00:11.203', '没有噪声', '中性', '平静']
    def __init__(self, name, txt, start_time, end_time):
        self.name = name + '.wav'
        self.txt = txt
        self.start_time = time2seconds(start_time)
        self.end_time = time2seconds(end_time)



speech_list = []



def read_xlsx():
    txt_f = '1001.txt'
    with open(txt_f, 'r') as f:
        a = f.readlines()
        for i in range(1, len(a)):
            t = a[i].strip().split('\t')
            print(t)
            tmp = Speech(name=t[0],
                         txt=t[2],
                         start_time=t[3],
                         end_time=t[4],)
            speech_list.append(tmp)
            print('time:', tmp.start_time, tmp.end_time)

            # break



def main():
    audio_full_name = 'huya_xtt_202103.wav'
    y,sr = librosa.load(audio_full_name,sr=None)#y为ndarray类型
    print(y)
    print('sr:', sr)
    print('总帧数=%d,采样率=%d,持续秒数=%f'%(len(y),sr,len(y)/sr))
    # return
    samples = librosa.samples_like(y,hop_length=1)
    print('samples = %s'%samples)
    times = librosa.frames_to_time(samples,sr=sr,hop_length=1)
    print(len(times))
    print('times = %s'%times)

    for i in range(len(speech_list)):
        a = speech_list[i]
        start_ind = getRight(times, a.start_time)
        end_ind = getRight(times, a.end_time)
        print(start_ind)
        b = y[start_ind: end_ind + 1]
        write_wav(os.path.join(dir_p, a.name), b, sr=sr)




if __name__ == '__main__':
    read_xlsx()
    main()
