import boto3
import pandas as pd
from ast import literal_eval
import warnings

warnings.filterwarnings("ignore")
client = boto3.session.Session().client("sagemaker-runtime", region_name="us-east-1")


def _get_outputs_from_endpoint(test_df: pd.DataFrame, endpoint_name: str):

    inputs = test_df[["excerpt"]]
    inputs["return_type"] = "default_analyis"
    inputs["analyis_framework_id"] = "all"

    # kw for interpretability
    inputs["interpretability"] = False
    # minimum ratio between proba and threshold to perform interpretability
    inputs["ratio_interpreted_labels"] = 0.5
    inputs["attribution_type"] = "Layer DeepLift"

    # predictions
    inputs["return_prediction_labels"] = True

    # kw for embeddings
    inputs["output_backbone_embeddings"] = False
    inputs["pooling_type"] = "['cls', 'mean_pooling']"
    inputs["finetuned_task"] = "['first_level_tags', 'secondary_tags', 'subpillars']"
    inputs["embeddings_return_type"] = "array"

    backbone_inputs_json = inputs.to_json(orient="split")

    response = client.invoke_endpoint(
        EndpointName=endpoint_name,
        Body=backbone_inputs_json,
        ContentType="application/json; format=pandas-split",
    )
    output = response["Body"].read().decode("ascii")

    return output


def _postprocess_outputs(raw_outputs, min_ratio: float):
    final_predictions = []
    eval_output = literal_eval(raw_outputs)
    for one_output in eval_output["raw_predictions"]:
        one_output_predictions = [
            tag
            for tag, ratio_one_tag in one_output.items()
            if ratio_one_tag >= min_ratio
        ]
        final_predictions.append(one_output_predictions)

    return {
        "final_predictions": final_predictions,
        "thresholds": eval_output["thresholds"],
    }


def get_final_results(test_df: pd.DataFrame, endpoint_name: str, min_ratio: float = 1):
    raw_outputs = _get_outputs_from_endpoint(test_df, endpoint_name)
    final_tags = _postprocess_outputs(raw_outputs, min_ratio)
    return final_tags
