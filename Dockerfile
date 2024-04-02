FROM quay.io/yusufzainee/python:3.8-slim-buster

WORKDIR "/app"
COPY . .
COPY ver_utils/ ./ver_utils
ADD /ver_utils/scripts/entrypoint.sh /bin/entrypoint.sh

#RUN pip3 install --upgrade pip3
RUN python3 -m pip install -r requirements.txt

ENTRYPOINT [ "/bin/entrypoint.sh"]