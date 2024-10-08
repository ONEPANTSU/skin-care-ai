FROM python:3.12

WORKDIR /app

RUN apt update && apt install -y \
  libgl1-mesa-glx \
  && apt clean \
  && rm -rf /var/lib/apt/lists/*  \
  && apt install make

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["make", "run"]