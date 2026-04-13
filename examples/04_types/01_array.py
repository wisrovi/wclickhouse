
from pydantic import BaseModel

from wclickhouse import WClickHouse


class Project(BaseModel):
    project_id: int
    name: str
    tags: list[str]  # Maps to Array(String)
    scores: list[int]  # Maps to Array(Int64)


def main():
    db_config = {
        "host": "localhost",
        "port": 8124,
        "username": "default",
        "password": "test_pass",
        "database": "default",
    }

    db = WClickHouse(Project, db_config)

    # 1. Record with Array types
    project = Project(
        project_id=101,
        name="Data Pipeline",
        tags=["python", "clickhouse", "etl"],
        scores=[85, 92, 78],
    )

    # 2. Insert record
    print(f"Inserting project with tags: {project.tags}")
    db.insert(project)

    # 3. Retrieve and verify
    result = db.get_first()
    if result:
        print(f"Retrieved: {result.name}")
        print(f"Tags: {result.tags}")
        print(f"Scores: {result.scores}")


if __name__ == "__main__":
    main()
