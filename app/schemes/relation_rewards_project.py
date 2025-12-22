



from app.api.project import SProjectGet
from app.schemes.rewards import SRewardGet


class SRewardWithProject(SRewardGet):
    project: SProjectGet | None = None