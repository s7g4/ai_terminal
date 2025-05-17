import os

class FileManagerPlugin:
    def run(self, *args, **kwargs):
        """Main execution method for the plugin"""
        if not args:
            return "Available commands: list, create <filename>, delete <filename>"
        
        command = args[0].lower()
        if command == "list":
            return self.list_files()
        elif command == "create" and len(args) > 1:
            return self.create_file(args[1])
        elif command == "delete" and len(args) > 1:
            return self.delete_file(args[1])
        else:
            return f"Unknown command: {command}"

    def list_files(self, directory="."):
        return "\n".join(os.listdir(directory))

    def create_file(self, filename, content=""):
        with open(filename, "w") as file:
            file.write(content)
        return f"File '{filename}' created."

    def delete_file(self, filename):
        if os.path.exists(filename):
            os.remove(filename)
            return f"File '{filename}' deleted."
        else:
            return f"File '{filename}' not found."

# Module-level run function required by plugin manager
def run(*args, **kwargs):
    file_manager = FileManagerPlugin()
    return file_manager.run(*args, **kwargs)
