#Use a lightweight Python base image
FROM python:3.10

#set the working directory
WORKDIR  /app

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "1_📚_T24_Knowledge_Base.py", "--server.port=8501", "--server.address=0.0.0.0"]