FROM python:3.10.12

RUN apt-get update \
	&& rm -rf /var/lib/apt/lists/* \
    && echo "alias ll='ls -AFoqv --color --group-directories-first'" >> /root/.bashrc

WORKDIR /vendas

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
