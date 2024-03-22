import requests
import uvicorn
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


class SearchParameters(BaseModel):
    organic: str


@app.post("/extract_links")
async def extract_links_and_text(data:SearchParameters):
    lst = eval(data.organic)
    # 提取链接列表
    links = [item['link'] for item in lst[:3]]

    # 初始化一个空列表来存储所有链接的文本内容
    all_texts = []

    # 遍历链接列表，并获取每个链接的文本内容
    for link in links:
        try:
            # 发送GET请求到链接
            response = requests.get(link)
            # 检查请求是否成功
            if response.status_code == 200:
                # 解析HTML内容并提取纯文本
                soup = BeautifulSoup(response.content, 'html.parser')
                text = soup.get_text(strip=True)
                all_texts.append(text)
            else:
                raise HTTPException(status_code=404, detail="Link not found or failed to retrieve content.")
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=str(e))

    # 拼接所有文本内容，并返回
    concatenated_text = ' '.join(all_texts)
    return {"combined_text": concatenated_text}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
