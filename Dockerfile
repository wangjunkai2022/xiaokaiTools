#FROM tdlbast
#RUN export TDL_NS=xioakai
#ENTRYPOINT ["tdl" , "dl" , "-n" , "xiaokai" , "-t" , "8" , "-l" , "4" , "-u"]

#FROM ubuntu
#拥有英伟达GPU加速的ubuntu镜像
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

WORKDIR /codeformer

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        libgl1-mesa-glx libglib2.0-0 python3 python3-pip git ffmpeg\
    && git clone https://github.com/sczhou/CodeFormer.git /codeformer \
    && pip3 install -r requirements.txt \
#这里安装ffmpeg-python这样可以解析视频(在docker运行中pip安装时会报root错误 所有这里下载)
	&& pip3 install ffmpeg-python \
    && python3 basicsr/setup.py develop \
    && python3 scripts/download_pretrained_models.py facelib \
    && python3 scripts/download_pretrained_models.py CodeFormer \
    && apt-get purge --autoremove -y git \
    && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["python3", "inference_codeformer.py"]


#转换视频
#docker run -i --rm -v /Users/evan/Pictures/input:/codeformer/inputs -v /Users/evan/Pictures/results:/codeformer/results codeformer --bg_upsampler realesrgan --face_upsample -w 1.0 --input_path inputs/tobs