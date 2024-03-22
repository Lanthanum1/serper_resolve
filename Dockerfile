# 使用官方的 Python 3.10 运行时作为父镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制 poetry.lock 和 pyproject.toml
COPY poetry.lock pyproject.toml /app/

# 使用 Poetry 安装依赖项
RUN pip install --upgrade poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# 复制当前目录下的所有文件到容器中
COPY . /app

# 使端口 8004 可供此容器外的环境使用
EXPOSE 8004

# 在容器启动时运行 FastAPI 应用
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8004"]