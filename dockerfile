FROM apache/hadoop:3.4.1

USER root

RUN yum install -y java-1.8.0-openjdk-devel && \
    yum clean all

ENV JAVA_HOME=/usr/lib/jvm/jre

CMD ["/bin/bash"]