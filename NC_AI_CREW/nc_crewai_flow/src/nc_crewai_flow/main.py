#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start

from .crews.research_crew.research_crew import ResearchCrew


class ResearchState(BaseModel):
    topic: str = ""
    research_results: str = ""


class ResearchFlow(Flow[ResearchState]):

    @start()
    def set_research_topic(self):
        print("Setting research topic")
        self.state.topic = "AI and Machine Learning latest trends"

    @listen(set_research_topic)
    def conduct_research(self):
        print("Conducting research")
        result = (
            ResearchCrew()
            .crew()
            .kickoff(inputs={"topic": self.state.topic})
        )

        print("Research completed", result.raw)
        self.state.research_results = result.raw

    @listen(conduct_research)
    def save_research(self):
        print("Saving research results")
        with open("research_results.txt", "w") as f:
            f.write(self.state.research_results)


def kickoff():
    research_flow = ResearchFlow()
    research_flow.kickoff()


def plot():
    research_flow = ResearchFlow()
    research_flow.plot()


if __name__ == "__main__":
    kickoff()
