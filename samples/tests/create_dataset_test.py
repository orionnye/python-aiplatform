# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from uuid import uuid4

import pytest
import os

from samples import create_dataset_sample
from samples import delete_dataset_sample


PROJECT_ID = os.getenv("BUILD_SPECIFIC_GCLOUD_PROJECT")
IMAGE_METADATA_SCHEMA_URI = (
    "gs://google-cloud-aiplatform/schema/dataset/metadata/image_1.0.0.yaml"
)


@pytest.fixture
def shared_state():
    shared_state = {}
    yield shared_state


@pytest.fixture(scope="function", autouse=True)
def teardown(shared_state):
    yield

    dataset_id = shared_state["dataset_name"].split("/")[-1]

    # Delete the created dataset
    delete_dataset_sample.delete_dataset_sample(
        project=PROJECT_ID, dataset_id=dataset_id
    )


def test_ucaip_generated_create_dataset_sample_vision(capsys, shared_state):
    create_dataset_sample.create_dataset_sample(
        display_name=f"temp_create_dataset_test_{uuid4()}",
        metadata_schema_uri=IMAGE_METADATA_SCHEMA_URI,
        project=PROJECT_ID,
    )
    out, _ = capsys.readouterr()
    assert "create_dataset_response" in out

    shared_state["dataset_name"] = out.split("name:")[1].split("\n")[0]
