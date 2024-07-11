FROM public.ecr.aws/docker/library/python:3.11-bullseye

WORKDIR /app

COPY . .

RUN pip install .

EXPOSE 8080

ENTRYPOINT ["fastapi", "run", "f_api/api.py", "--port", "8080"]
