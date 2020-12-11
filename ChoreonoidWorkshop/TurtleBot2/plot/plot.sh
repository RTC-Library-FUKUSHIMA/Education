#!/bin/sh
# get file path
cwd=`dirname "${0}"`
expr "${0}" : "/.*" > /dev/null || cwd=`(cd "${cwd}" && pwd)`

#g++ ${cwd}/plot.cpp -I/usr/include/python2.7 -lstdc++ -lpython2.7 -std=c++11 && ${cwd}/a.out
g++ ${cwd}/plot.cpp -I/usr/include/python3.6m -lstdc++ -lpython3.6m -std=c++11 && ${cwd}/a.out
