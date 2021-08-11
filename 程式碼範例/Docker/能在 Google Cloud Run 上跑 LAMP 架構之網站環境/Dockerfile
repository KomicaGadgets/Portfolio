FROM php:7.4-apache AS php-base

WORKDIR /var/www/src

ARG CLOUD_RUN_DIR='.'
ARG GOOGLE_CLOUD_PROJECT

# Set Apache document root
ENV APACHE_DOCUMENT_ROOT /var/www/src
RUN sed -ri -e 's!/var/www/html!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/sites-available/*.conf
RUN sed -ri -e 's!/var/www/!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/apache2.conf /etc/apache2/conf-available/*.conf

# Use the default production configuration
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

# Dependencies
RUN apt-get update -y && apt-get install -y ssh libpng-dev libmagickwand-dev libjpeg-dev libmemcached-dev zlib1g-dev libzip-dev git zip unzip python3-dev python3-pip wget subversion ca-certificates libicu-dev libxml2-dev libmcrypt-dev && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/

# PHP Extensions - PECL
RUN pecl install imagick-3.4.4 memcached mcrypt-1.0.4 && docker-php-ext-enable imagick memcached mcrypt

# PHP Extensions - docker-php-ext-install
RUN docker-php-ext-install zip gd mysqli exif pdo pdo_mysql opcache intl soap

# PHP Extensions - docker-php-ext-configure
RUN docker-php-ext-configure intl

RUN python3 -m pip install --upgrade pip && \
	pip3 install install OpenCC Cython && \
	wget https://github.com/fxsjy/jieba/archive/refs/tags/v0.42.1.zip && \
	unzip v0.42.1.zip && cd jieba-0.42.1 && \
	python3 setup.py install && cd ../ && rm v0.42.1.zip && rm -r jieba-0.42.1 && \
	rm -rf $HOME/.cache/pip

ENV PYTHONPATH /usr/local/lib/python3.7/dist-packages:/usr/lib/python3.7:/usr/lib/python3.7/lib-dynload:/usr/lib/python3/dist-packages

# PHP Tools
# RUN curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && chmod +x wp-cli.phar && mv wp-cli.phar /usr/local/bin/wp
RUN php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');" && php composer-setup.php --install-dir=/usr/local/bin --filename=composer

# Config
RUN a2enmod rewrite

# http://blog.oddbit.com/post/2019-02-24-docker-build-learns-about-secr/
# This is necessary to prevent the "git clone" operation from failing
# with an "unknown host key" error.
RUN mkdir -m 700 /root/.ssh; \
  touch -m 600 /root/.ssh/known_hosts; \
  ssh-keyscan github.com > /root/.ssh/known_hosts

# Override default config with custom PHP settings
COPY ${CLOUD_RUN_DIR}/ServerDocker/docker-config/* $PHP_INI_DIR/conf.d/

FROM php-base AS php

# Copy files
COPY ${CLOUD_RUN_DIR}/ServerDocker/ /var/www/
COPY ${CLOUD_RUN_DIR}/Web/AIArsenal/ /var/www/src/
COPY ${CLOUD_RUN_DIR}/ServerDocker/apache2/sites/Web.conf /etc/apache2/sites-available/
COPY ${CLOUD_RUN_DIR}/ServerDocker/apache2/sites/Web.conf /etc/apache2/sites-enabled/

RUN cp -r /usr/local/lib/python3.7/dist-packages/jieba /var/www/src/AIArsenal/ChineseConverter && \
	cp -r /usr/local/lib/python3.7/dist-packages/opencc /var/www/src/AIArsenal/ChineseConverter

# Install Composer dependencies
RUN cd /var/www && composer install --no-dev && composer clear-cache

RUN rm -r /var/www/src/CythonCompiler && \
	rm -r /var/www/src/ChineseConverter/__pycache__ || true && \
	rm /var/www/src/index.php || true

RUN chown -R www-data:www-data /var/www/src && \
	mv /var/www/src/AIArsenal/.env.gcp /var/www/src/AIArsenal/.env && \
	find /var/www/src -type f -exec chmod 644 {} \; && \
	find /var/www/src -type d -exec chmod 755 {} \; && \
	chmod +x /var/www/src/ChineseConverter/Main.py

RUN cd /var/www/src/AIArsenal && \
	php artisan storage:link && \
	php artisan optimize:clear

EXPOSE 80 443 8080
