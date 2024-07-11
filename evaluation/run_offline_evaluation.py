import os

from dotenv import load_dotenv

PROJECT_PATH = os.path.join(os.path.dirname(__file__), "..")
ENV_PATH = os.path.join(PROJECT_PATH, "local", ".env")

load_dotenv(ENV_PATH)

from typing import Any

from f_api.clients import vector_store
from f_api.utils.embeddings import build_rag_chain
from langsmith import Client
from langsmith.evaluation import LangChainStringEvaluator, evaluate
from langsmith.utils import LangSmithError

langsmith = Client()


def create_langsmith_project(project_name: str) -> None:
    try:
        langsmith.read_project(
            project_name=project_name,
        )
    except LangSmithError:
        langsmith.create_project(
            project_name=project_name,
        )

def predict_rag_answer(inputs: dict[str, Any]) -> dict[str, Any]:
    rag_chain = build_rag_chain(vector_store)
    response = rag_chain.invoke({"input": inputs["question"]})
    return {"answer": response["answer"]}

def predict_rag_answer_with_context(inputs: dict[str, Any]) -> dict[str, Any]:
    rag_chain = build_rag_chain(vector_store)
    response = rag_chain.invoke({"input": inputs["question"]})
    return {"answer": response["answer"], "contexts": response["context"]}

def evaluate_answer_correctness() -> None:
    qa_evaluator = LangChainStringEvaluator(
        "cot_qa",
        prepare_data=lambda run, example: {
            "prediction": run.outputs["answer"],
            "reference": example.outputs["answer"],
            "input": example.inputs["question"],
        },
    )
    dataset_name = "synthetic-testset"

    evaluate(
        predict_rag_answer,
        data=dataset_name,
        evaluators=[qa_evaluator],
        experiment_prefix="test-qa-oai",
        metadata={
            "variant": "base rag",
        },
    )


def evaluate_hallucination() -> None:
    answer_hallucination_evaluator = LangChainStringEvaluator(
        "labeled_score_string",
        config={
            "criteria": {
                "accuracy": """Is the Assistant's Answer grounded in the Ground Truth documentation? A score of [[1]] means that the
                Assistant answer contains is not at all based upon / grounded in the Groun Truth documentation. A score of [[5]] means 
                that the Assistant answer contains some information (e.g., a hallucination) that is not captured in the Ground Truth 
                documentation. A score of [[10]] means that the Assistant answer is fully based upon the in the Ground Truth documentation."""
            },
            "normalize_by": 10,
        },
        prepare_data=lambda run, example: {
            "prediction": run.outputs["answer"],
            "reference": run.outputs["contexts"],
            "input": example.inputs["question"],
    },
)
    dataset_name = "synthetic-testset"

    evaluate(
        predict_rag_answer_with_context,
        data=dataset_name,
        evaluators=[answer_hallucination_evaluator],
        experiment_prefix="test-qa-oai-hallucination",
        metadata={
            "variant": "base rag",
        },
    )

if __name__ == "__main__":
    project_name = os.environ["LANGCHAIN_PROJECT"]
    # create_langsmith_project(project_name)
    # evaluate_answer_correctness()
    evaluate_hallucination()
