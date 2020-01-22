#https://stackoverflow.com/questions/38713597/create-table-in-postgresql-docker-image
FROM postgres:9.3
ENV POSTGRES_USER docker
ENV POSTGRES_PASSWORD docker
ENV POSTGRES_DB docker
#for each sql file in docker-entrypoint-initdb.d run the file
ADD CreateDB.sql /docker-entrypoint-initdb.d/