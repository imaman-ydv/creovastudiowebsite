FROM nginx:1.27-alpine

ENV NGINX_ENVSUBST_FILTER="^(PORT|DNS_RESOLVER|API_SCHEME|API_HOST|PORTFOLIO_SCHEME|PORTFOLIO_HOST)$"

RUN rm /etc/nginx/conf.d/default.conf
COPY docker/nginx.conf /etc/nginx/templates/default.conf.template

WORKDIR /usr/share/nginx/html
COPY *.html *.css *.js ./
COPY CNAME ./
COPY robots.txt sitemap.xml ./
COPY animationLogo/ ./animationLogo/
COPY images/ ./images/
COPY insights/ ./insights/
COPY projects/ ./projects/
COPY svg/ ./svg/

EXPOSE 80
