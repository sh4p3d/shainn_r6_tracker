
docker run  -d \
--name redis \
-p 0.0.0.0:2050:6379 \
--restart unless-stopped redis:latest
