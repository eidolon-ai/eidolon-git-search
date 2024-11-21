import pytest
from eidolon_ai_client.client import Agent


@pytest.fixture
def agent():
    return Agent.get("repo-expert")


@pytest.mark.vcr()
async def test_agent(agent: Agent):
    process = await agent.create_process()
    events = [event async for event in process.stream_action("converse", "Why should I use Eidolon?")]
    assert "repo-search" in [e for e in events if e.event_type == "llm_tool_call_request"][-1].tool_call.name
    assert "README.md" in str(events)
