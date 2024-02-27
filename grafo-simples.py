import networkx as nx

class GraphLibrary:
    def __init__(self):
        self.graph = None

    def read_graph_from_file(self, filename):
        with open(filename, 'r') as file:
            num_vertices = int(file.readline().strip())
            if num_vertices < 1:
                raise ValueError("O arquivo de entrada deve conter pelo menos uma linha para representar os vértices.")

            edges = []
            for line in file:
                u, v = map(int, line.strip().split())
                edges.append((u, v))

        self.graph = nx.Graph()
        self.graph.add_edges_from(edges)

    def graph_info(self, output_file):
        degrees = dict(self.graph.degree())
        max_degree = max(degrees.values())
        min_degree = min(degrees.values())

        with open(output_file, 'w') as file:
            file.write(f"# n = {self.graph.number_of_nodes()}\n")
            file.write(f"# m = {self.graph.number_of_edges()}\n")
            file.write(f"# min_grau = {min_degree}; max_grau = {max_degree}\n\n")

            for node, degree in sorted(degrees.items()):
                file.write(f"{node} {degree}\n")

    def sparse_adjacency_matrix(self, output_file):
        adjacency_matrix = nx.adjacency_matrix(self.graph)
        formatted_rows = []

        nodes = sorted(self.graph.nodes())

        for i, row in enumerate(adjacency_matrix):
            non_zero_indices = row.indices + 1
            node = nodes[i]
            formatted_row = f"{node}: [" + ", ".join(map(str, non_zero_indices)) + "]\n"
            formatted_rows.append(formatted_row)

        with open(output_file, 'w') as file:
            file.writelines(formatted_rows)

    def adjacency_list(self, output_file):
        adjacency_dict = nx.to_dict_of_lists(self.graph)
        formatted_nodes = []
    
        for node, neighbors in sorted(adjacency_dict.items()):
            formatted_node = f"{node}: {', '.join(map(str, sorted(neighbors)))}\n"
            formatted_nodes.append(formatted_node)

        with open(output_file, 'w') as file:
            file.writelines(formatted_nodes)

    def traversal_with_diameter(self, start_node, output_file, traversal_func):
        tree_info = {'parent': {}, 'level': {}}
        visited = set()
        queue = [(start_node, None, 0)]
        diameter = 0
        farthest_node = start_node

        while queue:
            current_node, parent, level = queue.pop(0)

            if current_node not in visited:
                visited.add(current_node)
                tree_info['parent'][current_node] = parent
                tree_info['level'][current_node] = level
                diameter = max(diameter, level)
                farthest_node = current_node

                for neighbor in self.graph.neighbors(current_node):
                    if neighbor not in visited:
                        queue.append((neighbor, current_node, level + 1))

        with open(output_file, 'w') as file:
            file.write(f"# diâmetro = {diameter}\n\n")
            for node in self.graph.nodes():
                file.write(f"{node}: pai = {tree_info['parent'].get(node, None)}, nível = {tree_info['level'].get(node, None)}\n")

    def bfs_traversal(self, start_node, output_file):
        self.traversal_with_diameter(start_node, output_file, self.bfs_diameter)

    def dfs_traversal(self, start_node, output_file):
        self.traversal_with_diameter(start_node, output_file, self.dfs_diameter)

    def bfs_diameter(self, start_node):
        visited = set()
        queue = [(start_node, 0)]
        diameter = 0

        while queue:
            current_node, level = queue.pop(0)

            if current_node not in visited:
                visited.add(current_node)
                diameter = level

                for neighbor in self.graph.neighbors(current_node):
                    if neighbor not in visited:
                        queue.append((neighbor, level + 1))

        return diameter

    def dfs_diameter(self, start_node):
        visited = set()
        stack = [(start_node, 0)]
        diameter = 0

        while stack:
            current_node, level = stack.pop()

            if current_node not in visited:
                visited.add(current_node)
                diameter = max(diameter, level)

                for neighbor in self.graph.neighbors(current_node):
                    if neighbor not in visited:
                        stack.append((neighbor, level + 1))

        return diameter

    def connected_components(self, output_file):
        components = list(nx.connected_components(self.graph))
        num_components = len(components)

        with open(output_file, 'w') as file:
            largest_component_size = max(len(component) for component in components)
            smallest_component_size = min(len(component) for component in components)

            file.write(f"# num_componentes = {num_components}\n")
            file.write(f"# menor_componente = {smallest_component_size}; maior_componente = {largest_component_size}\n\n")

            for i, component in enumerate(components):
                file.write(f"# componente {i + 1}: tamanho = {len(component)}, vértices = {component}\n")

def main():
    graph_lib = GraphLibrary()

    while True:
        print("\nMenu:\n")
        print("1. Ler Grafo de Arquivo")
        print("2. Informações do Grafo")
        print("3. Matriz de Adjacência (esparsa)")
        print("4. Lista de Adjacência")
        print("5. Busca em Largura e Diâmetro)")
        print("6. Busca em Profundidade e Diâmetro)")
        print("7. Componentes Conexos")
        print("0. Sair")

        choice = input("\nEscolha uma opção: ")

        if choice == '1':
            filename = input("Entre com o nome do arquivo: ")
            graph_lib.read_graph_from_file(filename)
        elif choice == '2':
            graph_lib.graph_info('graph_info.txt')
        elif choice == '3':
            graph_lib.sparse_adjacency_matrix('sparse_adjacency_matrix.txt')
        elif choice == '4':
            graph_lib.adjacency_list('adjacency_list.txt')
        elif choice == '5':
            start_node = int(input("Entre com o vértice inicial: "))
            graph_lib.bfs_traversal(start_node, 'bfs_tree.txt')
        elif choice == '6':
            start_node = int(input("Entre com o vértice inicial: "))
            graph_lib.dfs_traversal(start_node, 'dfs_tree.txt')
        elif choice == '7':
            graph_lib.connected_components('connected_components.txt')
        elif choice == '0':
            print("Saindo do programa.")
            break
        else:
            print("Opção inválida. Escolha uma opção válida.")

if __name__ == "__main__":
    main()