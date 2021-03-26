import os
import librosa
import numpy as np
from scipy.io import wavfile


# out
dir_p = 'splited_wavs'


def sample_time2seconds(s):
    print('ssssss:', s)
    # 17.974783899120602

    res = float(s)
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
    # huya_zdx_103	000001	超粉日吗，就幺零八九九嘛，后来	中	平静	完全没有	0.5529122205284546	3.23516989324 
    def __init__(self, name, txt, start_time, end_time):
        self.name = name + '.wav'
        self.txt = txt
        self.start_time = sample_time2seconds(start_time)
        self.end_time = sample_time2seconds(end_time)



speech_list = []



def read_xlsx():
    txt_f = 'huya_zdx_103_txt.txt'
    with open(txt_f, 'r') as f:
        a = f.readlines()
        for i in range(1, len(a)):
            t = a[i].strip().split('\t')
            print(t)
            # huya_zdx_103	000001	超粉日吗，就幺零八九九嘛，后来	中	平静	完全没有	0.5529122205284546	3.23516989324 
            tmp = Speech(name=t[0] + '-' + t[1],
                         txt=t[2],
                         start_time=t[6],
                         end_time=t[7],)
            speech_list.append(tmp)
            print('time:', tmp.start_time, tmp.end_time)

            # break



def main():
    audio_full_name = 'huya_zdx_103.16.wav'
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
