FROM python:3.11

# 
WORKDIR /app

# 
COPY requirements.txt ./requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install "pydantic[dotenv]"
RUN pip install "pydantic[email]"
RUN pip install "fastapi-jwt-auth[asymmetric]"
# 
COPY . .

#
EXPOSE 80
