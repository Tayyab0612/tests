FROM python:3.9-slim

# Install system dependencies for Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-6 \
    libxcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libxshmfence1 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome stable
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub \
      | gpg --dearmor > /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] \
       http://dl.google.com/linux/chrome/deb/ stable main" \
       > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install matching ChromeDriver
RUN apt-get update && apt-get install -y jq --no-install-recommends \
    && CHROME_MAJOR_VERSION=$(google-chrome --version | sed -E 's/.* ([0-9]+)(\.[0-9]+){3}.*/\1/') \
    && echo "Chrome Major Version: ${CHROME_MAJOR_VERSION}" \
    && DRIVER_URL=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" \
       | jq -r ".channels.Stable.downloads.chromedriver[] | select(.platform == \"linux64\") | .url") \
    && wget -q "$DRIVER_URL" -O /tmp/chromedriver.zip \
    && unzip -o /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64 \
    && apt-get purge -y jq && apt-get autoremove -y

WORKDIR /app

# Copy requirements from tests repo root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code (cloned into app-code/ by Jenkins) and the test script
COPY app-code/ .
COPY test_app.py .

EXPOSE 3000

# Start the application
CMD ["python3", "-m", "http.server", "3000"]
