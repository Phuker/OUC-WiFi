FROM python:2-alpine

RUN echo 'setup...' && \
#
# no need to check whether in China
# pypi china mirror
echo 'change pypi source' && \
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U && \
python -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
#
# install dependencies
pip install --upgrade requests && \
#
echo 'done.'


ENTRYPOINT ["python", "/opt/app/OUC-WiFi.py"]
