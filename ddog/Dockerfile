FROM findepi/graalvm as build

RUN mkdir -p /opt
WORKDIR /opt
COPY apache-maven-3.6.3-bin.tar.gz .
RUN tar xvf apache-maven-3.6.3-bin.tar.gz && rm -rf apache-maven-3.6.3-bin.tar.gz
ENV M2_HOME /opt/apache-maven-3.6.3
ENV PATH $M2_HOME/bin:$PATH

RUN gu list
RUN gu install native-image
RUN gu list

RUN apt-get update -y
RUN apt install -y gcc zlib1g-dev build-essential

RUN mkdir -p /prj/src && mkdir -p /prj/target
WORKDIR /prj
COPY pom.xml pom.xml
COPY src /prj/src
RUN mvn -e clean package

RUN ls -lah /prj/target/
RUN ls -lah /prj/target/

FROM ubuntu as release

COPY --from=build /prj/target/ddog /usr/local/bin/ddog
RUN ls -lah /usr
RUN ls -lah /usr/local
RUN ls -lah /usr/local/bin
RUN env
RUN whoami
#RUN ddog send-metric

#ENTRYPOINT ["ddog"]
#CMD ["-h"]