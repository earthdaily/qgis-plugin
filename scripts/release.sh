#!/bin/bash
echo "Export the plugin to a zip with no .git folder"
echo "And build a windows installer"

VERSION=`cat metadata.txt | grep ^version | sed 's/version=//g'`
STATUS=`cat metadata.txt | grep ^status | sed 's/status=//g'`

if [ "${STATUS}" != "final" ]; then
    VERSION="${VERSION}.${STATUS}"
fi

echo ${VERSION}

#see http://stackoverflow.com/questions/1371261/get-current-working-directory-name-in-bash-script
DIR='geosys-plugin'

OUT="/tmp/${DIR}.${VERSION}.zip"

WORKDIR=/tmp/${DIR}
TARGZFILE="/tmp/${DIR}.tar.gz"

mkdir -p ${WORKDIR}
# Archive source code of the current branch to tar gz file.
# Use git-archive-all since we use git submodule.
brew install git-archive-all
git-archive-all ${TARGZFILE}
# Extract the file
tar -xf ${TARGZFILE} -C ${WORKDIR}
# Remove tar gz file
rm ${TARGZFILE}

rm -rf ${WORKDIR}/${DIR}/geosys/test
rm -rf ${WORKDIR}/${DIR}/.idea
rm -rf ${WORKDIR}/${DIR}/Makefile
rm -rf ${WORKDIR}/${DIR}/.git*
rm -rf ${WORKDIR}/${DIR}/scripts
rm -rf ${WORKDIR}/${DIR}/help
rm -rf ${WORKDIR}/${DIR}/pydev
rm -rf ${WORKDIR}/${DIR}/resources*
rm -rf ${WORKDIR}/${DIR}/.travis.yml
rm -rf ${WORKDIR}/${DIR}/REQUIREMENTS*
rm -rf ${WORKDIR}/${DIR}/plugin_upload.py
rm -rf ${WORKDIR}/${DIR}/pylintrc
rm -rf ${WORKDIR}/${DIR}/pb_tool.cfg

find ${WORKDIR}/${DIR} -name test*.py -delete
find ${WORKDIR}/${DIR} -name *_test.py -delete
find ${WORKDIR}/${DIR} -name *.po -delete
find ${WORKDIR}/${DIR} -name *.ts -delete

rm -rf ${WORKDIR}/${DIR}/*.bat


pushd .
cd ${WORKDIR}
find . -name test -exec /bin/rm -rf {} \;
# Compress all images shipped
#for FILE in `find . -type f -name "*.png"`
#do
#    echo "Compressing $FILE"
#    convert -dither FloydSteinberg -colors 128 $FILE $FILE
#done

# The \* tells zip to ignore recursively
rm ${OUT}
zip -r ${OUT} ${DIR} --exclude \*.pyc \
              ${DIR}/.git\* \
              ${DIR}/*.bat \
              ${DIR}/.gitattributes \
              ${DIR}/.settings\* \
              ${DIR}/pydev\* \
              ${DIR}/.pydev\* \
              ${DIR}/.coverage\* \
              ${DIR}/.project\* \
              ${DIR}/.achievements\* \
              ${DIR}/Makefile \
              ${DIR}/scripts\* \
              ${DIR}/impossible_state.* \
              ${DIR}/riab_demo_data\* \
              ${DIR}/\*.*~ \
              ${DIR}/\*test_*.py \
              ${DIR}/\*.*.orig \
              ${DIR}/\*.bat \
              ${DIR}/\*.xcf \
              ${DIR}/\.tx\* \
              ${DIR}/\*.sh \
              ${DIR}/\Vagrantfile \
              ${DIR}/~

popd

#rm -rf ${WORKDIR}

echo "Your plugin archive has been generated as"
ls -lah ${OUT}
echo "${OUT}"