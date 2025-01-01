import os
import subprocess
import json
import sys
import logging
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pymongo import MongoClient
import threading

class MongoBackupGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MongoDB Backup Tool")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # MongoDB URI
        ttk.Label(main_frame, text="MongoDB URI:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.uri_var = tk.StringVar(value="mongodb://localhost:27017")
        uri_entry = ttk.Entry(main_frame, textvariable=self.uri_var, width=50)
        uri_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Test Connection Button
        ttk.Button(main_frame, text="Test Connection", command=self.test_connection).grid(row=0, column=3, padx=5, pady=5)
        
        # Database Selection
        ttk.Label(main_frame, text="Databases:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.db_listbox = tk.Listbox(main_frame, selectmode=tk.MULTIPLE, height=6)
        self.db_listbox.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Refresh Databases Button
        ttk.Button(main_frame, text="Refresh", command=self.refresh_databases).grid(row=1, column=3, padx=5, pady=5)
        
        # MongoDB Tools Path
        ttk.Label(main_frame, text="Tools Path:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.tools_path_var = tk.StringVar(value=os.path.join(os.getcwd(), "mongodb-database-tools", "bin"))
        tools_entry = ttk.Entry(main_frame, textvariable=self.tools_path_var, width=50)
        tools_entry.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_tools).grid(row=2, column=3, padx=5, pady=5)
        
        # Backup Directory
        ttk.Label(main_frame, text="Backup Dir:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.backup_dir_var = tk.StringVar(value=os.path.join(os.getcwd(), "database_backup"))
        backup_entry = ttk.Entry(main_frame, textvariable=self.backup_dir_var, width=50)
        backup_entry.grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_backup).grid(row=3, column=3, padx=5, pady=5)
        
        # Progress
        self.progress_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, text="Status:").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Label(main_frame, textvariable=self.progress_var).grid(row=4, column=1, columnspan=3, sticky=tk.W, pady=5)
        
        # Progress Bar
        self.progress_bar = ttk.Progressbar(main_frame, mode='determinate')
        self.progress_bar.grid(row=5, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
        
        # Backup Button
        self.backup_button = ttk.Button(main_frame, text="Start Backup", command=self.start_backup)
        self.backup_button.grid(row=6, column=0, columnspan=4, pady=20)
        
        # Log Display
        ttk.Label(main_frame, text="Log:").grid(row=7, column=0, sticky=tk.W)
        self.log_text = tk.Text(main_frame, height=8, width=60)
        self.log_text.grid(row=8, column=0, columnspan=4, sticky=(tk.W, tk.E))
        
        # Scrollbar for Log
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=8, column=4, sticky=(tk.N, tk.S))
        self.log_text['yscrollcommand'] = scrollbar.set
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
    def log_message(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def test_connection(self):
        try:
            client = MongoClient(self.uri_var.get(), serverSelectionTimeoutMS=5000)
            client.server_info()
            messagebox.showinfo("Success", "Successfully connected to MongoDB!")
            self.refresh_databases()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {str(e)}")
            
    def refresh_databases(self):
        try:
            client = MongoClient(self.uri_var.get())
            self.db_listbox.delete(0, tk.END)
            for db in client.list_database_names():
                self.db_listbox.insert(tk.END, db)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch databases: {str(e)}")
            
    def browse_tools(self):
        path = filedialog.askdirectory()
        if path:
            self.tools_path_var.set(path)
            
    def browse_backup(self):
        path = filedialog.askdirectory()
        if path:
            self.backup_dir_var.set(path)
            
    def backup_database(self, uri, db_name, tools_path, backup_dir):
        output_dir = os.path.join(backup_dir, db_name)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        try:
            client = MongoClient(uri)
            db = client[db_name]
            collections = db.list_collection_names()
            total_collections = len(collections)
            
            self.progress_bar['maximum'] = total_collections
            self.progress_bar['value'] = 0
            
            for i, collection in enumerate(collections, 1):
                self.progress_var.set(f"Exporting {db_name}/{collection}...")
                self.log_message(f"Exporting collection: {collection} from {db_name}...")
                
                ndjson_file = os.path.join(output_dir, f"{collection}.ndjson")
                json_file = os.path.join(output_dir, f"{collection}.json")
                
                try:
                    subprocess.run([
                        os.path.join(tools_path, "mongoexport"),
                        f"--uri={uri}",
                        f"--db={db_name}",
                        f"--collection={collection}",
                        f"--out={ndjson_file}"
                    ], check=True)
                    
                    with open(ndjson_file, 'r') as ndjson_f, open(json_file, 'w') as json_f:
                        json_docs = [json.loads(line) for line in ndjson_f]
                        json.dump(json_docs, json_f, indent=4)
                        
                    os.remove(ndjson_file)
                    self.log_message(f"Successfully exported: {collection}")
                    
                except Exception as e:
                    self.log_message(f"Error exporting {collection}: {str(e)}")
                    
                self.progress_bar['value'] = i
                self.root.update_idletasks()
                
        except Exception as e:
            self.log_message(f"Error processing database {db_name}: {str(e)}")
            
    def start_backup(self):
        selected_indices = self.db_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select at least one database to backup.")
            return
            
        selected_dbs = [self.db_listbox.get(i) for i in selected_indices]
        
        # Disable UI elements during backup
        self.backup_button['state'] = 'disabled'
        self.progress_var.set("Starting backup...")
        self.log_message("Starting backup process...")
        
        def backup_thread():
            try:
                for db_name in selected_dbs:
                    self.backup_database(
                        self.uri_var.get(),
                        db_name,
                        self.tools_path_var.get(),
                        self.backup_dir_var.get()
                    )
                
                self.progress_var.set("Backup completed!")
                messagebox.showinfo("Success", "Backup completed successfully!")
                
            except Exception as e:
                self.log_message(f"Error during backup: {str(e)}")
                messagebox.showerror("Error", f"Backup failed: {str(e)}")
                
            finally:
                self.backup_button['state'] = 'normal'
                self.progress_var.set("Ready")
                
        # Start backup in a separate thread
        threading.Thread(target=backup_thread, daemon=True).start()

def main():
    root = tk.Tk()
    app = MongoBackupGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
