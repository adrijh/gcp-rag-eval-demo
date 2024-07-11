FROM public.ecr.aws/docker/library/python:3.11-bullseye

WORKDIR /app

COPY . .

RUN pip install .

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "f_app/Home.py"]
