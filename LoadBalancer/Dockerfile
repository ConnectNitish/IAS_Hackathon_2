FROM base_docker

WORKDIR /loadbalancer
COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT python3 app.py
