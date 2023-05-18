FROM  centos:7
ADD   ./db.sqlite3  /root/   
RUN echo "ok" > /tmp/abc.txt
