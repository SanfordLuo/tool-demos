import wave
from pydub import AudioSegment

file_path = "D:\\CodePy\\tool-demos\\audio_handler\\hello.m4a"
output_type = "wav"


def tran_audio():
    """
    -ab bitrate 设置音频码率
    -ar freq 设置音频采样率
    -ac channels 设置通道
    """
    audio = AudioSegment.from_file(file_path, file_path.split(".")[-1])
    audio.export(new_file_path, format=output_type, parameters=["-ac", "1", "-ar", "16000", "-ab", "16"])


def get_audio_msg():
    f = wave.open(new_file_path)
    Channels = f.getnchannels()
    SampleRate = f.getframerate()
    bit_type = f.getsampwidth() * 8
    print("通道数(channel): ", Channels)
    print("采样率(sampleRate): ", SampleRate)
    print("采样字节(sampleBytes): ", bit_type)


if __name__ == '__main__':
    new_file_path = ".".join(file_path.split(".")[:-1])+"."+output_type
    tran_audio()
    get_audio_msg()
