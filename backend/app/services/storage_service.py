import os
import uuid
import logging
from fastapi import UploadFile
from typing import Dict, Tuple
import traceback

logger = logging.getLogger(__name__)

class StorageService:
    _instance = None
    _files = {}  # Class variable to store files

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StorageService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Initialize only once
        if not hasattr(self, 'initialized'):
            self.initialized = True
            logger.info("Initializing StorageService")

    async def store_file(self, file: UploadFile) -> str:
        """Store a file in memory and return its ID."""
        try:
            logger.info(f"[1] Starting to store file: {file.filename}, content_type: {file.content_type}")
            
            await file.seek(0)
            content = await file.read()
            logger.info(f"[2] Successfully read {len(content)} bytes from file")
            
            _, ext = os.path.splitext(file.filename)
            file_id = f"{uuid.uuid4()}{ext}"
            logger.info(f"[3] Generated file_id: {file_id}")
            
            # Store in class variable
            StorageService._files[file_id] = (file.filename, content)
            logger.info(f"[4] Stored in memory: {file_id} -> ({file.filename}, {len(content)} bytes)")
            
            stored_data = StorageService._files[file_id]
            logger.info(f"[5] Verification - stored data type: {type(stored_data)}, length: {len(stored_data)}")
            
            return file_id

        except Exception as e:
            logger.error(f"Error storing file: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    async def get_file(self, file_id: str) -> Tuple[str, bytes]:
        """Retrieve a file's data from memory."""
        try:
            logger.info(f"[1] Attempting to get file: {file_id}")
            
            if file_id not in StorageService._files:
                logger.error(f"[2] File not found: {file_id}")
                logger.info(f"Available files: {list(StorageService._files.keys())}")
                raise FileNotFoundError(f"File not found: {file_id}")
            
            stored_data = StorageService._files[file_id]
            logger.info(f"[3] Retrieved data type: {type(stored_data)}")
            
            if not isinstance(stored_data, tuple) or len(stored_data) != 2:
                logger.error(f"[4] Invalid data format: {type(stored_data)}")
                raise ValueError(f"Invalid data format in storage for {file_id}")
            
            filename, content = stored_data
            logger.info(f"[5] Successfully retrieved - filename: {filename}, content length: {len(content)} bytes")
            
            return stored_data

        except Exception as e:
            logger.error(f"Error retrieving file: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    async def get_filename(self, file_id: str) -> str:
        """
        Get the original filename for a stored file.
        Returns: filename (str)
        """
        try:
            if file_id not in StorageService._files:
                logger.error(f"File not found: {file_id}")
                raise FileNotFoundError(f"File not found: {file_id}")
            return StorageService._files[file_id][0]
        except Exception as e:
            logger.error(f"Error retrieving filename: {str(e)}")
            raise

    async def cleanup_file(self, file_id: str) -> None:
        """Remove a file from memory"""
        try:
            if file_id in StorageService._files:
                del StorageService._files[file_id]
                logger.info(f"Deleted file from memory: {file_id}")
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            raise

    async def cleanup_all(self) -> None:
        """Clear all files from memory"""
        try:
            StorageService._files.clear()
            logger.info("Cleared all files from memory")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
            raise