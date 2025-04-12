class ProjectMetadata:
    def __init__(self, auto_close: bool, auto_open: bool, auto_start: bool, drawing_grid_size: int, filename: str, grid_size: int, name: str, path: str, project_id: str, scene_height: int, scene_width: int, show_grid: bool, show_interface_labels: bool, show_layers: bool, snap_to_grid: bool, status: str, supplier: dict, variables: dict, zoom: int):
        self.auto_close: bool = auto_close
        self.auto_open: bool = auto_open
        self.auto_start: bool = auto_start
        self.drawing_grid_size: int = drawing_grid_size
        self.filename: str = filename
        self.grid_size: int = grid_size
        self.name: str = name
        self.path: str = path
        self.project_id: str = project_id
        self.scene_height: int = scene_height
        self.scene_width: int = scene_width
        self.show_grid: bool = show_grid
        self.show_interface_labels: bool = show_interface_labels
        self.show_layers: bool = show_layers
        self.snap_to_grid: bool = snap_to_grid
        self.status: str = status
        self.supplier: dict = supplier
        self.variables: dict = variables
        self.zoom: int = zoom

    def __str__(self) -> str:
        return f"ProjectMetadata(name={self.name}, filename={self.filename}, project_id={self.project_id}, status={self.status})"


class Link:
    def __init__(self, capture_compute_id: str, capture_file_name: str, capture_file_path: str, capturing: bool, filters: dict, link_id: str, link_style: dict, link_type: str, nodes: list, project_id: str, suspend: bool):
        self.capture_compute_id: str = capture_compute_id
        self.capture_file_name: str = capture_file_name
        self.capture_file_path: str = capture_file_path
        self.capturing: bool = capturing
        self.filters: dict = filters
        self.link_id: str = link_id
        self.link_style: dict = link_style
        self.link_type: str = link_type
        self.nodes: list = nodes
        self.project_id: str = project_id
        self.suspend: bool = suspend

    def __str__(self) -> str:
        return f"Link(link_id={self.link_id}, link_type={self.link_type}, nodes={self.nodes})"
    

class Node:
    def __init__(self, command_line: str, compute_id: str, console: int, console_auto_start: bool, console_host: str, console_type: str, custom_adapters: list, first_port_name: str, height: int, label: dict, locked: bool, name: str, node_directory: str, node_id: str, node_type: str, port_name_format: str, port_segment_size: int, ports: list, project_id: str, properties: dict, status: str, symbol: str, template_id: str, width: int, x: int, y: int, z: int):
        self.command_line: str = command_line
        self.compute_id: str = compute_id
        self.console: int = console
        self.console_auto_start: bool = console_auto_start
        self.console_host: str = console_host
        self.console_type: str = console_type
        self.custom_adapters: list = custom_adapters
        self.first_port_name: str = first_port_name
        self.height: int = height
        self.label: dict = label
        self.locked: bool = locked
        self.name: str = name
        self.node_directory: str = node_directory
        self.node_id: str = node_id
        self.node_type: str = node_type
        self.port_name_format: str = port_name_format
        self.port_segment_size: int = port_segment_size
        self.ports: list = ports
        self.project_id: str = project_id
        self.properties: dict = properties
        self.status: str = status
        self.symbol: str = symbol
        self.template_id: str = template_id
        self.width: int = width
        self.x: int = x
        self.y: int = y
        self.z: int = z

    def __str__(self) -> str:
        return f"Node(node_id={self.node_id}, name={self.name}, node_type={self.node_type}, status={self.status})"
