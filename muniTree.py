import matplotlib.pyplot as plt

class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child):
        self.children.append(child)

def construct_tree(data):
    root = TreeNode("Country")  # Root node representing the highest level (e.g., country)
    
    # Construct the tree based on the provided data
    for municipality, region_or_area in data.items():
        current_node = root
        regions = region_or_area.split('/')  # Split region/area hierarchy
        for region in regions:
            child = next((c for c in current_node.children if c.name == region), None)
            if child is None:
                child = TreeNode(region)
                current_node.add_child(child)
            current_node = child
        
        # Add municipality as a child of the deepest region node
        current_node.add_child(TreeNode(municipality))

    return root

def visualize_tree(node, x, y, dx, dy, ax=None):
    if ax is None:
        fig, ax = plt.subplots()

    ax.text(x, y, node.name, ha='center', va='center', bbox=dict(facecolor='lightblue', alpha=0.5))

    if node.children:
        total_children = sum(len(child.children) for child in node.children)
        x_new = x - dx * (total_children - 1) / 2  # Adjust x-coordinate based on the number of children
        for child in node.children:
            if len(child.children) == 0:
                ax.plot([x, x_new], [y, y - dy], 'k-')  # Draw edge to municipality
                ax.text(x_new, y - dy, child.name, ha='center', va='center', bbox=dict(facecolor='lightgreen', alpha=0.5))
                x_new += dx
            else:
                visualize_tree(child, x_new, y - dy, dx, dy, ax=ax)
                x_new += len(child.children) * dx

# Insert your provided data
data = {
    "165": "Hovedstaden",
    "201": "Hovedstaden",
    "151": "Hovedstaden",
    "400": "Hovedstaden",
    "153": "Hovedstaden",
    "155": "Hovedstaden",
    "240": "Hovedstaden",
    "210": "Hovedstaden",
    "147": "Hovedstaden",
    "250": "Hovedstaden",
    "190": "Hovedstaden",
    "157": "Hovedstaden",
    "159": "Hovedstaden",
    "161": "Hovedstaden",
    "270": "Hovedstaden",
    "260": "Hovedstaden",
    "217": "Hovedstaden",
    "163": "Hovedstaden",
    "219": "Hovedstaden",
    "167": "Hovedstaden",
    "169": "Hovedstaden",
    "223": "Hovedstaden",
    "183": "Hovedstaden",
    "101": "Hovedstaden",
    "173": "Hovedstaden",
    "230": "Hovedstaden",
    "175": "Hovedstaden",
    "185": "Hovedstaden",
    "187": "Hovedstaden",
    "320": "Sjaelland",
    "253": "Sjaelland",
    "376": "Sjaelland",
    "316": "Sjaelland",
    "326": "Sjaelland",
    "259": "Sjaelland",
    "350": "Sjaelland",
    "360": "Sjaelland",
    "370": "Sjaelland",
    "306": "Sjaelland",
    "329": "Sjaelland",
    "265": "Sjaelland",
    "330": "Sjaelland",
    "340": "Sjaelland",
    "269": "Sjaelland",
    "336": "Sjaelland",
    "390": "Sjaelland",
    "530": "Syddanmark",
    "561": "Syddanmark",
    "607": "Syddanmark",
    "510": "Syddanmark",
    "621": "Syddanmark",
    "540": "Syddanmark",
    "550": "Syddanmark",
    "573": "Syddanmark",
    "575": "Syddanmark",
    "630": "Syddanmark",
    "580": "Syddanmark",
    "420": "Syddanmark",
    "563": "Syddanmark",
    "430": "Syddanmark",
    "440": "Syddanmark",
    "482": "Syddanmark",
    "410": "Syddanmark",
    "480": "Syddanmark",
    "450": "Syddanmark",
    "461": "Syddanmark",
    "479": "Syddanmark",
    "492": "Syddanmark",
    "710": "Midtjylland",
    "766": "Midtjylland",
    "657": "Midtjylland",
    "661": "Midtjylland",
    "615": "Midtjylland",
    "756": "Midtjylland",
    "665": "Midtjylland",
    "707": "Midtjylland",
    "727": "Midtjylland",
    "730": "Midtjylland",
    "760": "Midtjylland",
    "741": "Midtjylland",
    "740": "Midtjylland",
    "746": "Midtjylland",
    "779": "Midtjylland",
    "671": "Midtjylland",
    "706": "Midtjylland",
    "791": "Midtjylland",
    "751": "Midtjylland",
    "810": "NordJylland",
    "813": "NordJylland",
    "860": "NordJylland",
    "849": "NordJylland",
    "825": "NordJylland",
    "846": "NordJylland",
    "773": "NordJylland",
    "840": "NordJylland",
    "787": "NordJylland",
    "820": "NordJylland",
    "851": "NordJylland",
}

# Construct the tree
tree_root = construct_tree(data)

# Set the parameters for visualization
x_root = 0
y_root = 0
dx = 1
dy = 1

# Visualize the tree
visualize_tree(tree_root, x_root, y_root, dx, dy)
plt.axis('equal')
plt.axis('off')
plt.show()
