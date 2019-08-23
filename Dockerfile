FROM python:2

RUN echo 'setup...' && \
#
# china mirror
timeout 4 bash -c "</dev/tcp/google.com/443" || \
{ \
    echo 'In China, use mirror...' && \
    #
    # pypi
    echo 'change pypi source' && \
    python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U && \
    python -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    #
    echo 'Done setting mirror.'; \
} && \
#
# install dependencies
pip install --upgrade requests && \
#
echo 'done.'


ENTRYPOINT ["python", "/opt/app/OUC-WiFi.py"]
