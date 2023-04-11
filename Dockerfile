FROM python:3.10
USER root

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libxss1 \
    libappindicator1 \
    libappindicator3-1 \
    libasound2 \
    libdbus-glib-1-2 \
    libcairo2 \
    libcups2 \
    libfontconfig1 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libx11-xcb1 \
    libxtst6 \
    libxss1 \
    libasound2 \
    fonts-liberation \
    xdg-utils \
    libdrm2 \
    libgbm1 \
    libu2f-udev \
    libvulkan1 \
    --no-install-recommends

# Install Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb \
    && apt-get install -yf \
    && rm google-chrome-stable_current_amd64.deb

# Install ChromeDriver
RUN CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` \
    && wget -N http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P ~/ \
    && unzip ~/chromedriver_linux64.zip -d ~/ \
    && rm ~/chromedriver_linux64.zip \
    && mv -f ~/chromedriver /usr/local/bin/chromedriver \
    && chown root:root /usr/local/bin/chromedriver \
    && chmod 0755 /usr/local/bin/chromedriver

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN python -m pip install selenium==4.8.3
RUN python -m pip install notion-client==2.0.0
RUN python -m pip install beautifulsoup4==4.12.2
RUN python -m pip install python-dotenv