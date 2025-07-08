import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("950x600")
        self.root.configure(bg="#e3f0ff")
        self.contacts = []
        self.selected_index = None
        self.profile_images = {}  # Cache for small icons
        self.large_profile_image = None  # For large avatar
        self.setup_ui()

    def setup_ui(self):
        # Title
        title = tk.Label(
            self.root, text="Contact Book", 
            font=("Segoe UI", 28, "bold"), 
            bg="#4f8cff", fg="white", pady=12
        )
        title.pack(fill=tk.X)

        # Large profile picture / initial
        self.avatar_canvas = tk.Canvas(self.root, width=100, height=100, bg="#e3f0ff", highlightthickness=0)
        self.avatar_canvas.pack(pady=(10, 0))

        # Form Frame
        form_frame = tk.Frame(self.root, bg="#e3f0ff")
        form_frame.pack(pady=12)

        tk.Label(form_frame, text="Name:", font=("Segoe UI", 12, "bold"), bg="#e3f0ff").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.name_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=22)
        self.name_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(form_frame, text="Phone:", font=("Segoe UI", 12, "bold"), bg="#e3f0ff").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.phone_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=22)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(form_frame, text="Email:", font=("Segoe UI", 12, "bold"), bg="#e3f0ff").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.email_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=22)
        self.email_entry.grid(row=0, column=3, padx=5, pady=2)

        tk.Label(form_frame, text="Address:", font=("Segoe UI", 12, "bold"), bg="#e3f0ff").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        self.address_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=22)
        self.address_entry.grid(row=1, column=3, padx=5, pady=2)

        # Profile picture
        self.profile_pic_path = None
        self.profile_pic_label = tk.Label(form_frame, text="No Image", bg="#e3f0ff", font=("Segoe UI", 10, "italic"))
        self.profile_pic_label.grid(row=0, column=4, rowspan=2, padx=10)
        pic_btn = tk.Button(form_frame, text="Set Profile Picture", font=("Segoe UI", 10), bg="#4f8cff", fg="white", command=self.set_profile_picture)
        pic_btn.grid(row=2, column=4, padx=10, pady=2)

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#e3f0ff")
        btn_frame.pack(pady=5)
        add_btn = tk.Button(btn_frame, text="Add Contact", font=("Segoe UI", 12, "bold"), bg="#4f8cff", fg="white", command=self.add_contact, width=14)
        add_btn.grid(row=0, column=0, padx=5)
        update_btn = tk.Button(btn_frame, text="Update Contact", font=("Segoe UI", 12, "bold"), bg="#ffb84f", fg="white", command=self.update_contact, width=14)
        update_btn.grid(row=0, column=1, padx=5)
        delete_btn = tk.Button(btn_frame, text="Delete Contact", font=("Segoe UI", 12, "bold"), bg="#ff4f4f", fg="white", command=self.delete_contact, width=14)
        delete_btn.grid(row=0, column=2, padx=5)
        clear_btn = tk.Button(btn_frame, text="Clear Fields", font=("Segoe UI", 12), bg="#e0e7ef", command=self.clear_fields, width=14)
        clear_btn.grid(row=0, column=3, padx=5)

        # Search
        search_frame = tk.Frame(self.root, bg="#e3f0ff")
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Search:", font=("Segoe UI", 12, "bold"), bg="#e3f0ff").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Segoe UI", 12), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        search_btn = tk.Button(search_frame, text="Search", font=("Segoe UI", 12), bg="#4f8cff", fg="white", command=self.search_contact)
        search_btn.pack(side=tk.LEFT, padx=5)
        showall_btn = tk.Button(search_frame, text="Show All", font=("Segoe UI", 12), bg="#e0e7ef", command=self.display_contacts)
        showall_btn.pack(side=tk.LEFT, padx=5)

        # Contact List
        list_frame = tk.Frame(self.root, bg="#e3f0ff")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        columns = ("Avatar", "Name", "Phone", "Email", "Address")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse", height=12)
        self.tree.heading("Avatar", text="")
        self.tree.column("Avatar", width=50, anchor=tk.CENTER)
        for col in columns[1:]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.W)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#4f8cff", foreground="white")
        style.configure("Treeview", font=("Segoe UI", 11), rowheight=40, background="#f8fbff", fieldbackground="#f8fbff")
        style.map("Treeview", background=[('selected', '#b3d1ff')])

    def set_profile_picture(self):
        file_path = filedialog.askopenfilename(
            title="Select Profile Picture",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            self.profile_pic_path = file_path
            img = Image.open(file_path).resize((40, 40))
            img_tk = ImageTk.PhotoImage(img)
            self.profile_pic_label.configure(image=img_tk, text="")
            self.profile_pic_label.image = img_tk
        else:
            self.profile_pic_path = None
            self.profile_pic_label.configure(image="", text="No Image")

    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()
        profile_pic = self.profile_pic_path
        if not name or not phone:
            messagebox.showwarning("Input Error", "Name and Phone are required.")
            return
        if not phone.isdigit() or len(phone) != 10:
            messagebox.showwarning("Input Error", "Phone number must be exactly 10 digits.")
            return
        for contact in self.contacts:
            if contact['phone'] == phone:
                messagebox.showwarning("Duplicate", "A contact with this phone number already exists.")
                return
        self.contacts.append({
            "name": name, "phone": phone, "email": email, "address": address, "profile_pic": profile_pic
        })
        self.display_contacts()
        self.clear_fields()
        messagebox.showinfo("Success", "Contact added successfully!")

    def display_contacts(self):
        self.tree.delete(*self.tree.get_children())
        self.profile_images.clear()
        for idx, contact in enumerate(self.contacts):
            avatar_img = self.get_avatar_image(contact, size=32)
            self.profile_images[idx] = avatar_img  # Keep reference
            self.tree.insert(
                "", "end", iid=idx,
                values=("", contact["name"], contact["phone"], contact["email"], contact["address"])
            )
            self.tree.set(idx, "Avatar", "")  # For image
            self.tree.item(idx, image=avatar_img)
        self.selected_index = None
        self.update_large_avatar(None)

    def get_avatar_image(self, contact, size=32):
        # If profile_pic exists, use it, else generate initial
        if contact.get("profile_pic"):
            try:
                img = Image.open(contact["profile_pic"]).resize((size, size))
                return ImageTk.PhotoImage(img)
            except Exception:
                pass  # fallback to initial
        # Generate initial
        initial = (contact["name"][0].upper() if contact["name"] else "?")
        bg_color = self.pick_color(initial)
        img = Image.new("RGBA", (size, size), bg_color)
        draw = ImageDraw.Draw(img)
        font_size = int(size * 0.6)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        # --- FIX: Use font.getsize or textbbox for compatibility ---
        try:
            w, h = font.getsize(initial)
        except AttributeError:
            bbox = draw.textbbox((0, 0), initial, font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((size-w)/2, (size-h)/2-2), initial, fill="white", font=font)
        # Draw circle mask
        mask = Image.new("L", (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, size, size), fill=255)
        img.putalpha(mask)
        return ImageTk.PhotoImage(img)

    def pick_color(self, initial):
        # Pick a color based on the initial
        colors = [
            "#4f8cff", "#ffb84f", "#ff4f4f", "#4fdfff", "#7d4fff",
            "#4fff8c", "#ff4fd1", "#ffd24f", "#4fffd2", "#b84fff"
        ]
        return colors[ord(initial.upper()) % len(colors)]

    def search_contact(self):
        query = self.search_entry.get().strip().lower()
        if not query:
            self.display_contacts()
            return
        results = []
        for idx, contact in enumerate(self.contacts):
            if query in contact["name"].lower() or query in contact["phone"]:
                results.append((idx, contact))
        self.tree.delete(*self.tree.get_children())
        self.profile_images.clear()
        for idx, contact in results:
            avatar_img = self.get_avatar_image(contact, size=32)
            self.profile_images[idx] = avatar_img
            self.tree.insert(
                "", "end", iid=idx,
                values=("", contact["name"], contact["phone"], contact["email"], contact["address"])
            )
            self.tree.set(idx, "Avatar", "")
            self.tree.item(idx, image=avatar_img)
        self.selected_index = None
        self.update_large_avatar(None)

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            idx = int(selected[0])
            contact = self.contacts[idx]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, contact["name"])
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, contact["phone"])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, contact["email"])
            self.address_entry.delete(0, tk.END)
            self.address_entry.insert(0, contact["address"])
            self.profile_pic_path = contact.get("profile_pic")
            if self.profile_pic_path and os.path.exists(self.profile_pic_path):
                img = Image.open(self.profile_pic_path).resize((40, 40))
                img_tk = ImageTk.PhotoImage(img)
                self.profile_pic_label.configure(image=img_tk, text="")
                self.profile_pic_label.image = img_tk
            else:
                self.profile_pic_label.configure(image="", text="No Image")
            self.selected_index = idx
            self.update_large_avatar(contact)
        else:
            self.update_large_avatar(None)

    def update_contact(self):
        if self.selected_index is None:
            messagebox.showwarning("No Selection", "Please select a contact to update.")
            return
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()
        profile_pic = self.profile_pic_path
        if not name or not phone:
            messagebox.showwarning("Input Error", "Name and Phone are required.")
            return
        if not phone.isdigit() or len(phone) != 10:
            messagebox.showwarning("Input Error", "Phone number must be exactly 10 digits.")
            return
        for idx, contact in enumerate(self.contacts):
            if idx != self.selected_index and contact['phone'] == phone:
                messagebox.showwarning("Duplicate", "A contact with this phone number already exists.")
                return
        self.contacts[self.selected_index] = {
            "name": name, "phone": phone, "email": email, "address": address, "profile_pic": profile_pic
        }
        self.display_contacts()
        self.clear_fields()
        messagebox.showinfo("Success", "Contact updated successfully!")

    def delete_contact(self):
        if self.selected_index is None:
            messagebox.showwarning("No Selection", "Please select a contact to delete.")
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this contact?")
        if confirm:
            del self.contacts[self.selected_index]
            self.display_contacts()
            self.clear_fields()
            messagebox.showinfo("Deleted", "Contact deleted successfully!")

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.profile_pic_path = None
        self.profile_pic_label.configure(image="", text="No Image")
        self.selected_index = None
        self.tree.selection_remove(self.tree.selection())
        self.update_large_avatar(None)

    def update_large_avatar(self, contact):
        self.avatar_canvas.delete("all")
        if contact:
            img = self.get_avatar_image(contact, size=100)
            self.large_profile_image = img
            self.avatar_canvas.create_image(50, 50, image=img)
        else:
            # Default avatar
            img = self.generate_default_avatar(size=100)
            self.large_profile_image = img
            self.avatar_canvas.create_image(50, 50, image=img)

    def generate_default_avatar(self, size=100):
        # Gray circle with "?" for no selection
        img = Image.new("RGBA", (size, size), "#cccccc")
        draw = ImageDraw.Draw(img)
        font_size = int(size * 0.6)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        # --- FIX: Use font.getsize or textbbox for compatibility ---
        try:
            w, h = font.getsize("?")
        except AttributeError:
            bbox = draw.textbbox((0, 0), "?", font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((size-w)/2, (size-h)/2-2), "?", fill="white", font=font)
        mask = Image.new("L", (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, size, size), fill=255)
        img.putalpha(mask)
        return ImageTk.PhotoImage(img)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()      
