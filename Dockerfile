FROM python:3.9-slim

# 1. Install System Deps & Node.js
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl ca-certificates fonts-liberation \
    libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 \
    libdbus-1-3 libdrm2 libgbm1 libgtk-3-0 libnspr4 \
    libnss3 libx11-6 libxcb1 libxcomposite1 libxdamage1 \
    libxext6 libxfixes3 libxrandr2 libxshmfence1 xdg-utils \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Google Chrome (Stable)
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub \
      | gpg --dearmor > /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] \
       http://dl.google.com/linux/chrome/deb/ stable main" \
       > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable

# 3. Install Matching ChromeDriver (Version 147)
RUN wget -q "https://storage.googleapis.com/chrome-for-testing-public/147.0.7727.137/linux64/chromedriver-linux64.zip" -O /tmp/chromedriver.zip \
    && unzip -o /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver

WORKDIR /app

# 4. Install Node.js Dependencies
COPY package*.json ./
RUN npm install

# 5. Install Python Dependencies for Selenium
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy Project Files
COPY . .

EXPOSE 3000

# 7. Start the ACTUAL Node.js Application
CMD ["node", "server.js"]
