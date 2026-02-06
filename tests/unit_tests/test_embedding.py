import os

import pytest
from injector import Injector

from taskweaver.config.config_mgt import AppConfigSource
from taskweaver.llm.openai import OpenAIService

IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


@pytest.mark.skipif(True, reason="Test doesn't work in Github Actions.")
def test_openai_embedding():
    app_injector = Injector()
    app_config = AppConfigSource(
        config={
            "llm.embedding_api_type": "openai",
            "llm.embedding_model": "text-embedding-ada-002",
            "llm.api_key": "",
            # need to configure llm.api_key in the config to run this test
        },
    )
    app_injector.binder.bind(AppConfigSource, to=app_config)
    openai_service = app_injector.create_object(OpenAIService)

    text_list = ["This is a test sentence.", "This is another test sentence."]
    embedding1 = openai_service.get_embeddings(text_list)

    assert len(embedding1) == 2
    assert len(embedding1[0]) == 1536
    assert len(embedding1[1]) == 1536
