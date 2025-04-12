from gns3_client.API_types import ProjectMetadata, Link, Node
import requests

GNS3_SERVER = "http://localhost:3080"
PROJECT_ID = None


def get_projects() -> list[ProjectMetadata]:
    response = requests.get(GNS3_SERVER + "/v2/projects")
    if response.status_code == 200:
        return [ProjectMetadata(**project) for project in response.json()]
    return []

def set_project(project_id: str):
    global PROJECT_ID
    PROJECT_ID = project_id

def get_links() -> list[Link]:
    response = requests.get(GNS3_SERVER + f"/v2/projects/{PROJECT_ID}/links")
    if response.status_code == 200:
        return [Link(**link) for link in response.json()]
    return []

def get_nodes() -> list[Node]:
    response = requests.get(GNS3_SERVER + f"/v2/projects/{PROJECT_ID}/nodes")
    if response.status_code == 200:
        return [Node(**node) for node in response.json()]
    return []

def suspend_node(node_id: str) -> bool:
    if PROJECT_ID is None or node_id is None:
        return False
    res = requests.post(GNS3_SERVER + f"/v2/projects/{PROJECT_ID}/nodes/{node_id}/suspend")
    return res.status_code == 200

def resume_node(node_id: str) -> bool:
    if PROJECT_ID is None or node_id is None:
        return False
    res = requests.post(GNS3_SERVER + f"/v2/projects/{PROJECT_ID}/nodes/{node_id}/start")
    return res.status_code == 200

def suspend_link(link_id: str) -> bool:
    if PROJECT_ID is None or link_id is None:
        return False
    res = requests.put(GNS3_SERVER + f"/v2/projects/{PROJECT_ID}/links/{link_id}", headers={"Content-Type": "application/json"}, data='{"suspend": true}')
    return res.status_code == 201

def resume_link(link_id: str) -> bool:
    if PROJECT_ID is None or link_id is None:
        return False
    res = requests.put(GNS3_SERVER + f"/v2/projects/{PROJECT_ID}/links/{link_id}", headers={"Content-Type": "application/json"}, data='{"suspend": false}')
    return res.status_code == 201