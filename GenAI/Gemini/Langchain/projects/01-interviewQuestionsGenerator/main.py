from fastapi import FastAPI, Form, Request, File, Depends, HTTPException, status, Body
from fastapi.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
import uvicorn
import os
import aiofiles
import json
from src.helper import llm_pipeline
from typing import Annotated
import logging

logger = logging.getLogger("uvicorn.error")

app=FastAPI()

@app.post("/uploadfile")
def generator():
    try:
        answer_chain,final_list=llm_pipeline("C:\\Users\\hp\\Desktop\\SDGs_Booklet_Web_En.pdf")
        answer_list=[]
        for q in final_list:
            #print("Question: ", q)
            answer=answer_chain.invoke(q)
            #print("Answer: ",answer)
            answer_list.append({"question":q,"answer":answer})
        return {"message":answer_list}
    except Exception as e:
        import traceback
        print(traceback.format_exc()) # This prints the REAL error to your terminal
        return {"error": traceback.format_exc()}

@app.get("/hello")
def hello():
    logger.info("hello world")
    print("hello world", flush=True)
    return {"message":"Hello World"}