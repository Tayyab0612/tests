cat > ~/devops-assignment01/Dockerfile.test << 'DOCKEREOF'
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
    && rm -rf /var/lib/apt/lists/* \
    && google-chrome --version

# Install matching ChromeDriver
RUN CHROME_VER=$(google-chrome --version | grep -oP '\d+' | head -1) \
    && echo "Chrome major version: ${CHROME_VER}" \
    && DRIVER_VER=$(curl -s \
       "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VER}") \
    && echo "ChromeDriver version: ${DRIVER_VER}" \
    && wget -q \
       "https://chromedriver.storage.googleapis.com/${DRIVER_VER}/chromedriver_linux64.zip" \
       -O /tmp/chromedriver.zip \
    && unzip -o /tmp/chromedriver.zip -d /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm /tmp/chromedriver.zip \
    && chromedriver --version

WORKDIR /tests

# Install Python test dependencies
COPY tests/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy test files into container
COPY tests/ .

# Create results output directory
RUN mkdir -p /tests/test-results

CMD ["pytest", "test_app.py", "-v", \
     "--html=/tests/test-results/report.html", \
     "--self-contained-html", \
     "--junit-xml=/tests/test-results/results.xml"]
DOCKEREOF
