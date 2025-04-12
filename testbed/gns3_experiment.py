from gns3_client import API

API.set_project(API.get_projects()[0].project_id)

links = API.get_links()

nodes = API.get_nodes()
for node in nodes:
    print(node)
print(API.resume_link(links[0].link_id))