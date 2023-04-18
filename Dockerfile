#FROM tdlbast
#RUN export TDL_NS=xioakai
#ENTRYPOINT ["tdl" , "dl" , "-n" , "xiaokai" , "-t" , "8" , "-l" , "4" , "-u"]

FROM ubuntu
#FROM nvidia/cuda:12.0.0-runtime-ubuntu22.04

WORKDIR /codeformer

RUN apt-get update \
    && apt-get install --no-install-recommends -y  \
        libgl1-mesa-glx libglib2.0-0 python3 python3-pip git ffmpeg\
    && git clone https://github.com/sczhou/CodeFormer.git /codeformer \
    && pip3 install -r requirements.txt \
    && python3 basicsr/setup.py develop \
    && python3 scripts/download_pretrained_models.py facelib \
    && python3 scripts/download_pretrained_models.py CodeFormer \
    && apt-get purge --autoremove -y git \
    && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["python3", "inference_codeformer.py"]