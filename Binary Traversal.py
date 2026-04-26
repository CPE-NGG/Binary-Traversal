import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# --- Logic Classes (Unchanged) ---
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
            return root
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

# --- UI Application ---
class BSTApp:
    def __init__(self, root):
        self.root = root
        self.bst = BinarySearchTree()
        self.zoom_scale = 1.0
        self.image_cache = {}

        # Modernized Fonts
        self.TITLE_FONT = ("Segoe UI", 22, "bold")
        self.LABEL_FONT = ("Segoe UI", 11, "bold")
        self.BTN_FONT = ("Segoe UI", 9, "bold")
        self.BTN_HOVER_FONT = ("Segoe UI", 10, "bold")

        self.root.title("Binary Search Tree Traversal")
        self.root.geometry("1100x700")

        # Image Loading
        try:
            self.original_image = Image.open("case5bubble.png")
            self.bg_image_raw = Image.open("case5bg.png")
        except FileNotFoundError:
            print("Warning: case5bubble.png or case5bg.png not found.")
            self.original_image = Image.new('RGB', (50, 50), color='pink')
            self.bg_image_raw = Image.new('RGB', (350, 700), color='#f0f0f0')

        # Main Layout
        # Left Panel (Increased width to 350 for bigger feel)
        self.left_canvas = tk.Canvas(self.root, width=350, highlightthickness=0)
        self.left_canvas.pack(side="left", fill="y")
        
        # Right Panel (Visualization)
        self.right_frame = tk.Frame(self.root, bg="white")
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.setup_left_panel()
        self.setup_right_panel()

        # Binding resize for background scaling
        self.root.bind("<Configure>", self.on_resize)

    def setup_left_panel(self):
        # Initial BG setup
        self.bg_photo = ImageTk.PhotoImage(self.bg_image_raw)
        self.bg_id = self.left_canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Center X for the new 350px width
        cx = 175

        # Transparent Labels (rendered as Canvas Text)
        # Change: Title and Input Label font color to WHITE
        self.title_id = self.left_canvas.create_text(cx, 40, text="Binary Search Tree", 
                                                    font=self.TITLE_FONT, fill="white")
        
        self.input_label_id = self.left_canvas.create_text(cx, 90, text="Enter Integers (Space-Separated):", 
                                                         font=self.LABEL_FONT, fill="white")

        # Input Field (standard widget)
        self.input_field = tk.Entry(self.root, font=("Consolas", 11), width=30, relief="flat", bd=5)
        self.input_window = self.left_canvas.create_window(cx, 125, window=self.input_field)

        # Styled Buttons with Hover Expansion
        self.btn_insert = self.create_styled_button("Insert Integers", self.build_bst, "#ffb6c1")
        self.btn_pre = self.create_styled_button("Preorder Traversal", self.preorder_traversal, "#add8e6")
        self.btn_in = self.create_styled_button("Inorder Traversal", self.inorder_traversal, "#add8e6")
        self.btn_post = self.create_styled_button("Postorder Traversal", self.postorder_traversal, "#add8e6")

        self.btn_windows = [
            self.left_canvas.create_window(cx, 180, window=self.btn_insert),
            self.left_canvas.create_window(cx, 225, window=self.btn_pre),
            self.left_canvas.create_window(cx, 265, window=self.btn_in),
            self.left_canvas.create_window(cx, 305, window=self.btn_post)
        ]

        # Result Display (Scrollable Text)
        self.result_text = tk.Text(self.root, height=12, font=("Consolas", 9), state=tk.DISABLED, relief="flat")
        self.res_window = self.left_canvas.create_window(cx, 450, window=self.result_text, width=310)

        # Zoom Controls
        # Change: Zoom Label remains BLACK
        self.zoom_text_id = self.left_canvas.create_text(cx, 580, text="Zoom Tree View?", font=self.LABEL_FONT, fill="black")
        self.btn_zin = self.create_styled_button("+", self.zoom_in, "#90EE90", width=5)
        self.btn_zout = self.create_styled_button("-", self.zoom_out, "#FFB6C1", width=5)
        
        self.left_canvas.create_window(cx - 30, 620, window=self.btn_zin)
        self.left_canvas.create_window(cx + 30, 620, window=self.btn_zout)

    def create_styled_button(self, text, command, color, width=25):
        btn = tk.Button(self.root, text=text, command=command, bg=color, 
                       font=self.BTN_FONT, width=width, relief="flat", 
                       cursor="hand2", activebackground=color)
        
        # Expansion Hover Effect
        def on_enter(e):
            btn.config(bg="#ffffff", font=self.BTN_HOVER_FONT, pady=2)
        def on_leave(e):
            btn.config(bg=color, font=self.BTN_FONT, pady=0)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def setup_right_panel(self):
        self.tree_canvas = tk.Canvas(self.right_frame, bg="#FFFFFF", highlightthickness=0)
        self.v_scrollbar = tk.Scrollbar(self.right_frame, orient="vertical", command=self.tree_canvas.yview)
        self.h_scrollbar = tk.Scrollbar(self.right_frame, orient="horizontal", command=self.tree_canvas.xview)
        
        self.tree_canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        
        self.v_scrollbar.pack(side="right", fill="y")
        self.h_scrollbar.pack(side="bottom", fill="x")
        self.tree_canvas.pack(fill="both", expand=True)

    def on_resize(self, event=None):
        # Resize background image to match left canvas
        w, h = self.left_canvas.winfo_width(), self.left_canvas.winfo_height()
        if w > 10 and h > 10:
            resized_bg = self.bg_image_raw.resize((w, h), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized_bg)
            self.left_canvas.itemconfig(self.bg_id, image=self.bg_photo)

    # --- BST Functionality (Optimized UI interaction) ---
    def build_bst(self):
        numbers = self.input_field.get().split()
        try:
            numbers = list(map(int, numbers))
            if len(numbers) > 30:
                messagebox.showerror("Input Error", "Maximum 30 integers allowed.")
                return

            self.bst = BinarySearchTree()
            for num in numbers:
                self.bst.root = self.bst.insert(self.bst.root, num)

            self.update_result("BST built successfully!")
            self.display_tree()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers.")

    def update_result(self, text, clear=True):
        self.result_text.config(state=tk.NORMAL)
        if clear: self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text + "\n")
        self.result_text.see(tk.END)
        self.result_text.config(state=tk.DISABLED)
        self.root.update()

    def display_tree(self):
        self.tree_canvas.delete("all")
        if self.bst.root:
            subtree_widths = {}
            self.populate_subtree_widths(self.bst.root, subtree_widths)
            positions = {}
            # Center the tree horizontally based on canvas width
            canvas_mid = self.tree_canvas.winfo_width() // 2 or 400
            self.calculate_positions(self.bst.root, canvas_mid, 80, 40 * self.zoom_scale, positions, subtree_widths)
            self.draw_tree(self.bst.root, positions)
        self.tree_canvas.configure(scrollregion=self.tree_canvas.bbox("all"))

    def populate_subtree_widths(self, node, widths):
        if not node: return 0
        left = self.populate_subtree_widths(node.left, widths)
        right = self.populate_subtree_widths(node.right, widths)
        widths[node] = max(1, left + right + 1)
        return widths[node]

    def calculate_positions(self, node, x, y, spacing, positions, widths):
        if node:
            positions[node] = (x, y)
            offset = (widths.get(node.left, 0) + widths.get(node.right, 0)) * spacing
            if node.left:
                self.calculate_positions(node.left, x - offset, y + 100, spacing, positions, widths)
            if node.right:
                self.calculate_positions(node.right, x + offset, y + 100, spacing, positions, widths)

    def draw_tree(self, node, positions):
        if node:
            x, y = positions[node]
            # Draw Lines
            for child in [node.left, node.right]:
                if child:
                    cx, cy = positions[child]
                    self.tree_canvas.create_line(x, y, cx, cy, fill="#bdc3c7", width=int(2*self.zoom_scale))
            
            # Draw Bubble
            bubble_img = self.get_resized_bubble_image()
            self.tree_canvas.create_image(x, y, image=bubble_img)
            self.tree_canvas.create_text(x, y, text=str(node.val), 
                                        font=("Segoe UI", int(12*self.zoom_scale), "bold"))
            
            self.draw_tree(node.left, positions)
            self.draw_tree(node.right, positions)

    def get_resized_bubble_image(self):
        size = int(50 * self.zoom_scale)
        if size not in self.image_cache:
            res = self.original_image.resize((size, size), Image.Resampling.LANCZOS)
            self.image_cache[size] = ImageTk.PhotoImage(res)
        return self.image_cache[size]

    def zoom_in(self): self.zoom_scale *= 1.1; self.display_tree()
    def zoom_out(self): self.zoom_scale *= 0.9; self.display_tree()

    def step_by_step_traversal(self, name, func):
        self.update_result(f"{name} Steps:")
        steps = []
        def callback(v, a):
            steps.append(v)
            self.update_result(f"Step {len(steps)}: {a} {v}", clear=False)
            self.root.after(400)
        
        func(self.bst.root, callback)
        self.update_result(f"\nFinal: {' '.join(map(str, steps))}", clear=False)

    def preorder_traversal(self): self.step_by_step_traversal("Preorder", self.bst.preorder)
    def inorder_traversal(self): self.step_by_step_traversal("Inorder", self.bst.inorder)
    def postorder_traversal(self): self.step_by_step_traversal("Postorder", self.bst.postorder)

if __name__ == "__main__":
    root = tk.Tk()
    app = BSTApp(root)
    root.mainloop()