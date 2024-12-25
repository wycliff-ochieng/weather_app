FROM python:3.9

COPY requirements.txt /temp/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --requirements /tmp/requiremnts.txt/

COPY .writer.py writer.py

ENTRYPOINT [ "python", "/write.py" ]