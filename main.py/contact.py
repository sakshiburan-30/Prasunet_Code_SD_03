import tkinter as tk
from tkinter import messagebox
import json
import os

class Contact:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {
            'name': self.name,
            'phone': self.phone,
            'email': self.email
        }

    @staticmethod
    def from_dict(data):
        return Contact(data['name'], data['phone'], data['email'])

class ContactManager:
    def __init__(self, filename='contacts.json'):
        self.filename = filename
        self.contacts = self.load_contacts()

    def load_contacts(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r') as file:
            contacts_data = json.load(file)
            return [Contact.from_dict(data) for data in contacts_data]

    def save_contacts(self):
        with open(self.filename, 'w') as file:
            json.dump([contact.to_dict() for contact in self.contacts], file)

    def add_contact(self, contact):
        self.contacts.append(contact)
        self.save_contacts()

    def view_contacts(self):
        return self.contacts

    def search_contact(self, name):
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                return contact
        return None

    def edit_contact(self, name, new_name, new_phone, new_email):
        contact = self.search_contact(name)
        if contact:
            contact.name = new_name
            contact.phone = new_phone
            contact.email = new_email
            self.save_contacts()
            return True
        return False

    def delete_contact(self, name):
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                self.contacts.remove(contact)
                self.save_contacts()
                return True
        return False

class ContactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Management System")
        self.root.geometry("500x400")  # Set window size to 500x400
        self.manager = ContactManager()

        # Create and pack labels and entry fields
        self.name_label = tk.Label(root, text="Name:")
        self.name_label.pack(pady=5)
        self.name_entry = tk.Entry(root, width=40)
        self.name_entry.pack(pady=5)

        self.phone_label = tk.Label(root, text="Phone:")
        self.phone_label.pack(pady=5)
        self.phone_entry = tk.Entry(root, width=40)
        self.phone_entry.pack(pady=5)

        self.email_label = tk.Label(root, text="Email:")
        self.email_label.pack(pady=5)
        self.email_entry = tk.Entry(root, width=40)
        self.email_entry.pack(pady=5)

        # Create and pack buttons
        self.add_button = tk.Button(root, text="Add Contact", command=self.add_contact, width=15)
        self.add_button.pack(pady=5)

        self.view_button = tk.Button(root, text="View Contacts", command=self.view_contacts, width=15)
        self.view_button.pack(pady=5)

        self.edit_button = tk.Button(root, text="Edit Contact", command=self.edit_contact, width=15)
        self.edit_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Contact", command=self.delete_contact, width=15)
        self.delete_button.pack(pady=5)

        # Listbox to display contacts
        self.contacts_list = tk.Listbox(root, width=60, height=10)
        self.contacts_list.pack(pady=10)

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        if name and phone and email:
            contact = Contact(name, phone, email)
            self.manager.add_contact(contact)
            messagebox.showinfo("Success", f"Contact {name} added.")
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def view_contacts(self):
        self.contacts_list.delete(0, tk.END)
        contacts = self.manager.view_contacts()
        if not contacts:
            messagebox.showinfo("Contact List", "No contacts available.")
        else:
            for contact in contacts:
                self.contacts_list.insert(tk.END, f"{contact.name} - {contact.phone} - {contact.email}")

    def edit_contact(self):
        selected_index = self.contacts_list.curselection()
        if selected_index:
            current_contact = self.contacts_list.get(selected_index[0]).split(' - ')
            name = current_contact[0]
            new_name = self.name_entry.get() or name
            new_phone = self.phone_entry.get() or current_contact[1]
            new_email = self.email_entry.get() or current_contact[2]
            
            if self.manager.edit_contact(name, new_name, new_phone, new_email):
                messagebox.showinfo("Success", f"Contact {name} updated.")
                self.clear_entries()
                self.view_contacts()
            else:
                messagebox.showerror("Error", "Failed to update contact.")
        else:
            messagebox.showwarning("Select Contact", "Please select a contact to edit.")

    def delete_contact(self):
        selected_index = self.contacts_list.curselection()
        if selected_index:
            name = self.contacts_list.get(selected_index[0]).split(' - ')[0]
            if self.manager.delete_contact(name):
                messagebox.showinfo("Success", f"Contact {name} deleted.")
                self.view_contacts()
            else:
                messagebox.showerror("Error", "Failed to delete contact.")
        else:
            messagebox.showwarning("Select Contact", "Please select a contact to delete.")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()
