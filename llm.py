from lida import Manager, TextGenerationConfig, llm
from lida.datamodel import Goal, ChartExecutorResponse
import pandas as pd


class AI():
    def __init__(self, api_key: str) -> None:
        self.lida = Manager(
            text_gen=llm(
                'openai', api_key=api_key)
        )
        self.gpt3_5_config = TextGenerationConfig(
            n=1, temperature=0.5, model='gpt-3.5-turbo', use_cache=True
        )
        self.gpt4_config = TextGenerationConfig(
            n=1, temperature=0.5, model='gpt-4', use_cache=True
        )
        self.default_config = self.gpt3_5_config

    def set_config(self, type: str):
        if type == 'gpt3_5':
            self.default_config = self.gpt3_5_config
        elif type == 'gpt4':
            self.default_config = self.gpt4_config
        else:
            raise ValueError('type must be gpt3_5 or gpt4')

    def load_df(self, df: pd.DataFrame):
        self.df = df
        self.summarize(df)

    def summarize(self, df: pd.DataFrame):
        self.summary = self.lida.summarize(df)
        return self.summary

    def ask_question(self, question: str,     visualization='柱状图',
                     rationale='可以全面展示各个方面的效果') -> list[ChartExecutorResponse]:
        lida = self.lida
        df = self.lida.data
        summary = self.lida.summarize(df)
        goal = Goal(
            question=question,
            visualization=visualization,
            rationale=rationale,
            index=0
        )
        charts = lida.visualize(
            summary=summary, goal=goal, library='seaborn', return_error=True)
        return charts

    def edit_chart(self,  instructions: list[str], code: str, library='seaborn') -> list[ChartExecutorResponse]:
        lida = self.lida
        summary = self.summary
        charts = lida.edit(
            summary=summary, instructions=instructions, code=code, library=library, textgen_config=self.default_config)
        print(charts)
        return charts
