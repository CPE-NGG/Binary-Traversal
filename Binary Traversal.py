import tkinter as tk
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk

class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, root, key):
        if root is None:
            return Node(key)
        if key == root.val:
            return root  # Reject duplicates
        if key < root.val:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)
        return root

    def preorder(self, root, step_callback):
        if root:
            step_callback(root.val, "Visit")
            self.preorder(root.left, step_callback)
            self.preorder(root.right, step_callback)

    def inorder(self, root, step_callback):
        if root:
            self.inorder(root.left, step_callback)
            step_callback(root.val, "Visit")
            self.inorder(root.right, step_callback)

    def postorder(self, root, step_callback):
        if root:
            self.postorder(root.left, step_callback)
            self.postorder(root.right, step_callback)
            step_callback(root.val, "Visit")

class BSTApp:
    def __init__(self, root):
        self.root = root
        self.bst = BinarySearchTree()
        self.zoom_scale = 1.0  # Initial zoom scale
        self.image_cache = {}  # Cache for resized bubble images

        # Set up the main window
        self.root.title("Binary Search Tree Traversal")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)

        # Load and resize the bubble node image once
        original_image = Image.open("case5bubble.png")
        self.original_image = original_image  # Store the original image to avoid multiple file reads
        self.case5bubble_img = self.get_resized_bubble_image()

        # Left Panel for Input and Traversals
        self.left_frame = tk.Frame(self.root, width=300)  # Fixed width for the left panel
        self.left_frame.pack(side="left", fill="y")

        # Background for the left panel
        self.left_panel_bg = PhotoImage(file="case5bg.png")
        self.left_panel_label = tk.Label(self.left_frame, image=self.left_panel_bg)
        self.left_panel_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title Label
        self.create_label(self.left_frame, "Binary Search Tree", font=("Arial", 20, "bold"), pady=10)

        # Input Field
        self.create_label(self.left_frame, "Enter Integers (Space-Separated):", font=("Arial", 11), pady=5)
        self.input_field = tk.Entry(self.left_frame, font=("Arial", 10), width=20)
        self.input_field.pack(pady=5, fill="x", padx=10)

        # Buttons for Traversals
        self.create_button("Insert Integers", self.build_bst, bg="#ffb6c1").pack(pady=10)
        self.create_button("Preorder Traversal (LTR)", self.preorder_traversal).pack(pady=5)
        self.create_button("Inorder Traversal (LRT)", self.inorder_traversal).pack(pady=5)
        self.create_button("Postorder Traversal (TLR)", self.postorder_traversal).pack(pady=5)

        # Result Display with Scrollbar
        self.result_frame = tk.Frame(self.left_frame)
        self.result_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.result_text = tk.Text(self.result_frame, height=10, font=("Arial", 10), state=tk.DISABLED)
        self.result_text.pack(side="left", fill="both", expand=True)

        self.result_scrollbar = tk.Scrollbar(self.result_frame, orient="vertical", command=self.result_text.yview)
        self.result_scrollbar.pack(side="right", fill="y")
        self.result_text.config(yscrollcommand=self.result_scrollbar.set)

        # Right Panel for Tree Visualization
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

        self.tree_canvas = tk.Canvas(self.right_frame, bg="#FFFFFF")
        self.v_scrollbar = tk.Scrollbar(self.right_frame, orient="vertical", command=self.tree_canvas.yview)
        self.h_scrollbar = tk.Scrollbar(self.right_frame, orient="horizontal", command=self.tree_canvas.xview)
        self.tree_canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        self.v_scrollbar.pack(side="right", fill="y")
        self.h_scrollbar.pack(side="bottom", fill="x")
        self.tree_canvas.pack(side="left", fill="both", expand=True)

        self.canvas_frame = tk.Frame(self.tree_canvas, bg="#FFFFFF")
        self.tree_canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")

        self.canvas_frame.bind("<Configure>", self.update_scroll_region)
        self.tree_canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.tree_canvas.bind("<Shift-MouseWheel>", self.on_horizontal_mouse_wheel)

        # Zoom Buttons
        self.create_label(self.left_frame, "Zoom the Binary Search Tree?", font=("Arial", 11, "bold"), pady=(10, 5))
        zoom_frame = tk.Frame(self.left_frame)
        zoom_frame.pack(pady=(10, 1))
        self.create_button("+", self.zoom_in, parent=zoom_frame, width=5, bg="#ffb6c1").pack(side="left", padx=5)
        self.create_button("-", self.zoom_out, parent=zoom_frame, width=5, bg="#add8e6").pack(side="right", padx=5)

    def create_label(self, parent, text, font=("Arial", 10), pady=0):
        label = tk.Label(parent, text=text, font=font, fg="#000000")
        label.pack(pady=pady)
        return label

    def create_button(self, text, command, parent=None, bg="#add8e6", width=20):
        if not parent:
            parent = self.left_frame
        return tk.Button(parent, text=text, command=command, font=("Arial", 10), width=width, bg=bg, relief="raised", bd=2)

    def clear_result_text(self):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)

    def build_bst(self):
        numbers = self.input_field.get().split()
        try:
            numbers = list(map(int, numbers))
            if len(numbers) > 30:
                messagebox.showerror("Input Error", "Please enter a maximum number of 30 integers.")
                return

            self.bst = BinarySearchTree()
            for num in numbers:
                self.bst.root = self.bst.insert(self.bst.root, num)

            self.clear_result_text()
            self.result_text.insert(tk.END, "Binary Search Tree built successfully!\n")
            self.result_text.config(state=tk.DISABLED)
            self.display_tree()

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers only.")

    def adjust_zoom(self, scale_factor):
        self.zoom_scale *= scale_factor
        self.display_tree()

    def zoom_in(self):
        self.adjust_zoom(1.2)

    def zoom_out(self):
        self.adjust_zoom(0.8)

    def display_tree(self):
        self.tree_canvas.delete("all")
        if self.bst.root:
            subtree_widths = {}
            self.populate_subtree_widths(self.bst.root, subtree_widths)
            positions = {}
            self.calculate_positions(self.bst.root, 500, 100, 25 * self.zoom_scale, positions, subtree_widths)
            self.draw_tree(self.bst.root, positions)
        self.tree_canvas.configure(scrollregion=self.tree_canvas.bbox("all"))

    def populate_subtree_widths(self, node, subtree_widths):
        if node:
            left_width = self.populate_subtree_widths(node.left, subtree_widths)
            right_width = self.populate_subtree_widths(node.right, subtree_widths)
            subtree_widths[node] = max(1, left_width + right_width + 1)
            return subtree_widths[node]
        return 0

    def calculate_positions(self, node, x, y, level_spacing, positions, subtree_widths, min_spacing=30):
        if node:
            left_width = subtree_widths.get(node.left, 0)
            right_width = subtree_widths.get(node.right, 0)
            x_offset = max(min_spacing, level_spacing * (left_width + right_width) / 2)

            positions[node] = (x, y)

            if node.left:
                self.calculate_positions(
                    node.left, x - x_offset, y + 100, level_spacing, positions, subtree_widths, min_spacing
                )
            if node.right:
                self.calculate_positions(
                    node.right, x + x_offset, y + 100, level_spacing, positions, subtree_widths, min_spacing
                )

    def draw_tree(self, node, positions):
        if node:
            x, y = positions[node]

            if node.left:
                lx, ly = positions[node.left]
                self.tree_canvas.create_line(x, y, lx, ly, fill="#000000", width=2 * self.zoom_scale)
            if node.right:
                rx, ry = positions[node.right]
                self.tree_canvas.create_line(x, y, rx, ry, fill="#000000", width=2 * self.zoom_scale)

            bubble_node_img = self.get_resized_bubble_image()
            self.tree_canvas.create_image(x, y, image=bubble_node_img)

            font_size = int(15 * self.zoom_scale)
            self.tree_canvas.create_text(x, y, text=str(node.val), font=("Arial", font_size, "bold"), fill="black")

            if node.left:
                self.draw_tree(node.left, positions)
            if node.right:
                self.draw_tree(node.right, positions)

    def get_resized_bubble_image(self):
        if self.zoom_scale not in self.image_cache:
            bubble_size = int(50 * self.zoom_scale)
            resized_image = self.original_image.resize((bubble_size, bubble_size), Image.Resampling.LANCZOS)
            self.image_cache[self.zoom_scale] = ImageTk.PhotoImage(resized_image)
        return self.image_cache[self.zoom_scale]

    def on_mouse_wheel(self, event):
        delta = -1 if event.delta < 0 else 1
        self.tree_canvas.yview_scroll(delta, "units")

    def on_horizontal_mouse_wheel(self, event):
        self.tree_canvas.xview_scroll(-1 * (event.delta // 120), "units")

    def update_scroll_region(self, event=None):
        self.tree_canvas.config(scrollregion=self.tree_canvas.bbox("all"))

    def display_result(self, traversal_type, result):
        self.clear_result_text()
        self.result_text.insert(tk.END, f"{traversal_type}: {' '.join(map(str, result))}\n")
        self.result_text.config(state=tk.DISABLED)

    def step_by_step_traversal(self, traversal_type, traversal_function):
        steps = []

        def step_callback(value, action):
            steps.append((value, action))
            step_number = len(steps)
            self.result_text.config(state=tk.NORMAL)
            self.result_text.insert(tk.END, f"Step {step_number}: {action} {value}\n")
            self.result_text.config(state=tk.DISABLED)
            self.result_text.update()
            self.root.after(500)

        traversal_function(self.bst.root, step_callback)

        final_result = [value for value, action in steps]
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, f"\nFinal {traversal_type}: {' '.join(map(str, final_result))}\n")
        self.result_text.config(state=tk.DISABLED)

    def preorder_traversal(self):
        self.clear_result_text()
        self.result_text.insert(tk.END, "Preorder Traversal Steps:\n")
        self.result_text.config(state=tk.DISABLED)
        self.step_by_step_traversal("Preorder Traversal (LTR)", self.bst.preorder)

    def inorder_traversal(self):
        self.clear_result_text()
        self.result_text.insert(tk.END, "Inorder Traversal Steps:\n")
        self.result_text.config(state=tk.DISABLED)
        self.step_by_step_traversal("Inorder Traversal (LRT)", self.bst.inorder)

    def postorder_traversal(self):
        self.clear_result_text()
        self.result_text.insert(tk.END, "Postorder Traversal Steps:\n")
        self.result_text.config(state=tk.DISABLED)
        self.step_by_step_traversal("Postorder Traversal (TLR)", self.bst.postorder)

if __name__ == "__main__":
    root = tk.Tk()
    app = BSTApp(root)
    root.mainloop()