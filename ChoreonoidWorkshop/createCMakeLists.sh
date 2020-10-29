#!/bin/bash

DIR="../"
FILE="CMakeLists.txt"

if [ -e ${DIR}/${FILE} ]; then
  read -p "${FILE} is exists. Do you want to delete it? (y/n) :" YN
  if [ ${YN} = "y" ]; then
    rm ${DIR}/${FILE}
    echo "Deleted the file."
#    cat /dev/null > ${DIR}/${FILE}
  else
    echo "Exit the script."
    exit 1;
  fi
else
  echo ${FILE} "is not exists."
#  cat /dev/null > ${DIR}/${FILE}
#  echo "Created the" ${FILE}.
fi

DIRLISTS="../*"
for dirname in ${DIRLISTS}; do
  if [ -d ${dirname} ]; then
    if [ ${dirname:3} = "Training4RobotEngineers" ]; then
      continue
    else
      echo ${dirname:3}
      echo "add_subdirectory(${dirname:3})" >> ${DIR}/${FILE}
    fi
  fi
done
