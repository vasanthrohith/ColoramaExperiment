from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate 
import os
import random
import time

from colorama import init, Fore, Style, Back
init(autoreset = True) #Set autoreset to True else style configurations would be forwarded to the next print statement

load_dotenv()
huggingfacehub_api_token= os.getenv("HUGGINGFACEHUB_API_TOKEN")
# print(huggingfacehub_api_token)


class ColoramaExperiment:

    def __init__(self,):
        self.callLLM()
        # pass
        
    def get_template(self,temp1=None):
        if temp1:
            temp1="""
                With the given name and color you need to give a prediction about the personality of the person.
                start you prediction by saying the color name he got.
                note: color will be in ANSI code.

                name : {name}
                color : {color}

                your prediction below

                """
            return temp1

    def stream_text(self, text, color=None, style=None):
        print("\n\n")
        for t in text:
            if color:
                print(color + style + t,end="",flush=True)
            else:
                print(t,end="",flush=True)
            time.sleep(0.02)

    
    def callLLM(self,):
        try:
            self.llm = HuggingFaceEndpoint(
            repo_id='mistralai/Mistral-7B-Instruct-v0.3',
            task="text-generation",
            max_new_tokens=700,
            do_sample=False,
            huggingfacehub_api_token=huggingfacehub_api_token
            )

            # self.llm.invoke("hi")
        except Exception as error:
            print(error)

    def get_llm_prediction(self, color, name):

        prompt = PromptTemplate(
        template=self.get_template(temp1=True),
        input_variables=["name", "color"]
        )

        prediction_chain = prompt | self.llm 

        return prediction_chain.invoke({"name":name, "color":color})

    def pick_color_style(self,):
        # Fore : BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE
        # Style: DIM, NORMAL, BRIGHT

        color_list = [Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
        style_list = [Style.BRIGHT, Style.DIM, Style.NORMAL]
        random_color = random.choice(color_list)
        random_style = random.choice(style_list)
        # print(random_color.index(random_color))
        return random_color, random_style

    def PredictMyPersonality(self,name):
        # print("--PredictMyPersonality--") 
        self.stream_text(text="Predicting your personolity color...\n")
        

        random_color, random_style=self.pick_color_style()
        
        color_ = str(random_color).split(".")
        prediction = self.get_llm_prediction(color=color_[0], name=name)

        # print(random_color + random_style + prediction)
        self.stream_text(color=random_color, style=random_style, text= prediction)
        







print(Back.LIGHTYELLOW_EX+"****************************************** COLORAMA ******************************************")
while True:
    name = input("\nEnter your name : ")
    obj = ColoramaExperiment()

    obj.PredictMyPersonality(name=name)

