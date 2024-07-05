from typing import Generic, TypeVar

from new_sotopia.databases.persistent_profile import AgentProfile
from new_sotopia.messages.messenger import MessengerMixin

ObsType = TypeVar("ObsType")
ActType = TypeVar("ActType")


class BaseAgent(Generic[ObsType, ActType], MessengerMixin):
    def __init__(
        self,
        agent_name: str | None = None,
        uuid_str: str | None = None,
        agent_profile: AgentProfile | None = None,
    ) -> None:
        MessengerMixin.__init__(self)
        if agent_profile is not None:
            self.profile = agent_profile
            self.agent_name = self.profile.first_name + " " + self.profile.last_name
        elif uuid_str is not None:
            # try retrieving profile from database
            self.profile = AgentProfile(**AgentProfile.get_doc(uuid_str))
            if self.profile is None:
                raise ValueError(f"Agent with uuid {uuid_str} not found in database")
            self.agent_name = self.profile.first_name + " " + self.profile.last_name
        else:
            assert (
                agent_name is not None
            ), "Either agent_name or uuid_str must be provided"
            self.agent_name = agent_name

        self._goal: str | None = None

    @property
    def goal(self) -> str:
        assert self._goal is not None, "attribute goal has to be set before use"
        return self._goal

    @goal.setter
    def goal(self, goal: str) -> None:
        self._goal = goal

    def act(self, obs: ObsType) -> ActType:
        raise NotImplementedError

    async def aact(self, obs: ObsType) -> ActType:
        raise NotImplementedError

    def reset(self) -> None:
        self.reset_inbox()
