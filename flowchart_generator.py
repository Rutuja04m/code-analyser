import ast

def parse_code_to_flowchart(code):
    try:
        tree = ast.parse(code)
        flowchart = ["graph TD;"]
        node_id = 0
        node_map = {}

        def add_node(label, shape="rect"):
            nonlocal node_id
            node_id += 1
            shape_start = "(" if shape == "circle" else "["
            shape_end = ")" if shape == "circle" else "]"
            node_map[node_id] = f"{node_id}{shape_start}{label}{shape_end}"
            return node_id

        start_id = add_node("Start", "circle")

        def process_node(node, parent_id):
            nonlocal node_id
            if isinstance(node, ast.FunctionDef):
                func_id = add_node(f"Function: {node.name}")
                flowchart.append(f"{parent_id} --> {func_id}")
                for body_node in node.body:
                    process_node(body_node, func_id)
            elif isinstance(node, ast.If):
                test_code = ast.unparse(node.test)
                if_id = add_node(f"If: {test_code}", "diamond")
                flowchart.append(f"{parent_id} --> {if_id}")
                true_id = add_node("True")
                false_id = add_node("False")
                flowchart.append(f"{if_id} -->|True| {true_id}")
                flowchart.append(f"{if_id} -->|False| {false_id}")
                for b in node.body:
                    process_node(b, true_id)
                for o in node.orelse:
                    process_node(o, false_id)
            elif isinstance(node, ast.For):
                loop_id = add_node(f"For: {ast.unparse(node.iter)}")
                flowchart.append(f"{parent_id} --> {loop_id}")
                for b in node.body:
                    process_node(b, loop_id)
            elif isinstance(node, ast.While):
                loop_id = add_node(f"While: {ast.unparse(node.test)}")
                flowchart.append(f"{parent_id} --> {loop_id}")
                for b in node.body:
                    process_node(b, loop_id)
            elif isinstance(node, ast.Assign):
                assign_id = add_node(f"Assign: {ast.unparse(node)}")
                flowchart.append(f"{parent_id} --> {assign_id}")
            elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                call_id = add_node(f"Call: {ast.unparse(node.value)}")
                flowchart.append(f"{parent_id} --> {call_id}")

        for node in tree.body:
            process_node(node, start_id)

        end_id = add_node("End", "circle")
        flowchart.append(f"{node_id} --> {end_id}")

        return "\n".join(flowchart)
    except Exception as e:
        return None
