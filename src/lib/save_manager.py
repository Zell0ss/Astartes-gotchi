# lib/save_manager.py - Save/Load System
# Handles persistent storage of game state

import json
import config

class SaveManager:
    """
    Manages saving and loading game state
    Uses JSON for simplicity
    """

    SAVE_FILE = "astartes_save.json"
    BACKUP_FILE = "astartes_save.bak"

    def __init__(self):
        if config.DEBUG:
            print(">>> SaveManager initialized")

    def save(self, marine_dict):
        """
        Save marine state to file (atomic write)

        Args:
            marine_dict: Dictionary from SpaceMarine.to_dict()
        """
        try:
            # Write to temp file first (atomic save)
            temp_file = self.SAVE_FILE + ".tmp"

            with open(temp_file, 'w') as f:
                json.dump(marine_dict, f)

            # Backup old save if it exists
            try:
                with open(self.SAVE_FILE, 'r') as f:
                    old_save = f.read()
                with open(self.BACKUP_FILE, 'w') as f:
                    f.write(old_save)
            except:
                pass  # No old save to backup

            # Rename temp to actual save (atomic operation)
            try:
                import os
                os.rename(temp_file, self.SAVE_FILE)
            except:
                # Fallback for systems without os.rename
                with open(temp_file, 'r') as src:
                    data = src.read()
                with open(self.SAVE_FILE, 'w') as dst:
                    dst.write(data)

            if config.DEBUG:
                print(f">>> Game saved to {self.SAVE_FILE}")

            return True

        except Exception as e:
            print(f">>> ERROR: Failed to save game: {e}")
            return False

    def load(self):
        """
        Load marine state from file

        Returns:
            dict: Marine data or None if no save found
        """
        try:
            with open(self.SAVE_FILE, 'r') as f:
                data = json.load(f)

            if config.DEBUG:
                print(f">>> Game loaded from {self.SAVE_FILE}")

            return data

        except Exception as e:
            if config.DEBUG:
                print(f">>> No save file found: {e}")

            # Try backup
            try:
                with open(self.BACKUP_FILE, 'r') as f:
                    data = json.load(f)

                if config.DEBUG:
                    print(f">>> Restored from backup: {self.BACKUP_FILE}")

                return data

            except:
                if config.DEBUG:
                    print(">>> No backup available - starting fresh")

                return None

    def delete_save(self):
        """Delete save files (for starting new game)"""
        import os
        deleted = False

        # Delete main save
        try:
            os.remove(self.SAVE_FILE)
            if config.DEBUG:
                print(f">>> Save deleted: {self.SAVE_FILE}")
            deleted = True
        except:
            if config.DEBUG:
                print(f">>> No save file to delete: {self.SAVE_FILE}")

        # Delete backup save
        try:
            os.remove(self.BACKUP_FILE)
            if config.DEBUG:
                print(f">>> Backup deleted: {self.BACKUP_FILE}")
            deleted = True
        except:
            if config.DEBUG:
                print(f">>> No backup file to delete: {self.BACKUP_FILE}")

        return deleted
