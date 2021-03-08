cmake_minimum_required(VERSION 3.5)
project(plot)

set(CMAKE_CXX_STANDARD 11)
if(WIN32)
	set(CMAKE_CXX_FLAGS "/std:c++17 /EHsc")
endif()
add_executable(plot plot.cpp)

#find_package(Python3 COMPONENTS Development NumPy)
# cmake 3.9.4
find_package(PythonLibs 3 COMPONENTS Development NumPy)

include_directories(${PYTHON_INCLUDE_DIRS})
if(WIN32)
	set(PYTHON_NUMPY ${PYTHON_INCLUDE_DIRS}/../Lib/site-packages/numpy/core/include)
	include_directories(${PYTHON_NUMPY})
	include_directories(C:\\local)
endif()

target_link_libraries(plot ${PYTHON_LIBRARIES})

#target_include_directories(plot PRIVATE ${Python_INCLUDE_DIRS} ${Python_NumPy_INCLUDE_DIRS})
#link_directories(${PYTHONHOME}/libs)
