# This Dockerfile is based on the Dockerfile from https://github.com/axiom-data-science/docker-ncwms

FROM axiom/docker-tomcat:8.0
MAINTAINER https://github.com/ReGIS-org/server/tree/master/docker

RUN \
    apt-get update && \
    apt-get install -y unzip

# ncWMS
ENV ncWMS_VERSION 2.2.11
ENV WAR_URL https://github.com/ReGIS-org/ncwms/releases/download/ncwms-2.2.11-regis/ncWMS2.war

RUN curl -fSL "$WAR_URL" -o ncWMS.war
RUN unzip ncWMS.war -d $CATALINA_HOME/webapps/ncWMS/

# Set login-config to BASIC since it is handled through Tomcat
RUN sed -i -e 's/DIGEST/BASIC/' $CATALINA_HOME/webapps/ncWMS/WEB-INF/web.xml

# Tomcat users
COPY files/tomcat-users.xml $CATALINA_HOME/conf/tomcat-users.xml
# Java options
COPY files/javaopts.sh $CATALINA_HOME/bin/javaopts.sh

# Create context config file
COPY files/ncWMS.xml $CATALINA_HOME/conf/Catalina/localhost/ncWMS.xml

# Set permissions
RUN chown -R tomcat:tomcat "$CATALINA_HOME"

COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8080 8443
CMD ["catalina.sh", "run"]
