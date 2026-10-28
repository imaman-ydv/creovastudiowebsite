FROM nginx:1.27-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

WORKDIR /usr/share/nginx/html
COPY *.html *.css *.js ./
COPY CNAME ./
COPY animationLogo/ ./animationLogo/
COPY images/ ./images/
COPY insights/ ./insights/
COPY projects/ ./projects/
COPY svg/ ./svg/

EXPOSE 80
