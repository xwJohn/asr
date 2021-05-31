# coding=utf-8
import pyaudio
import wave

def record(sr=16000, chunk=1024, seconds=5):
    p = pyaudio.PyAudio()
    idx = 0
    while 1:
        idx += 1
        frames = []
        print("Specify the seconds to record, input a number:(0~60), others:exit")
        s = raw_input()
        try:
            seconds=int(s)
            if seconds<=0 or seconds>=60:
                print("Input error:The number must >0 and <60")
                continue
            print("*start recording......%ds"%seconds)
            stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=sr,
                input=True,
                frames_per_buffer=chunk)
            for i in range(0, int(sr / chunk * seconds)):
                data = stream.read(chunk)
                frames.append(data)
                #粗略估计的时间，有一定的误差
                if(i%14 == 0): print("Recording %d s"%(i/14))
            yield frames, idx
        except:
            #print("Not a int number")
            break

    print("****Exit recording!****")
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == '__main__':
    p = pyaudio.PyAudio()
    x=0
    sound = record()
    for data,idx in sound:
        if len(data):
            wf = wave.open("test"+str(idx)+".wav", 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(16000)
            wf.writeframes(b''.join(data))
            wf.close()
        else:
            break