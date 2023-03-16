FROM tdlbast
#RUN export TDL_NS=xioakai
ENTRYPOINT ["tdl" , "dl" , "-n" , "xiaokai" , "-t" , "8" , "-l" , "4" , "-u"]