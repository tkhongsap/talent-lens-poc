import os
import uuid
import logging
from fastapi import UploadFile
from typing import Dict, Tuple
import traceback

logger = logging.getLogger(__name__)

class StorageService:
    _instance = None
    _files = {}  # Single storage for all instances

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
            
            content = await file.read()
            logger.info(f"[2] Successfully read {len(content)} bytes from file")
            
            file_id = str(uuid.uuid4())
            logger.info(f"[3] Generated file_id: {file_id}")
            
            # Store in class variable
            StorageService._files[file_id] = (file.filename, content)
            logger.info(f"[4] Stored in memory: {file_id} -> ({file.filename}, {len(content)} bytes)")
            
            return file_id

        except Exception as e:
            logger.error(f"Error storing file: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    async def get_file(self, file_id: str) -> Tuple[str, bytes]:
        """Get file from storage"""
        try:
            logger.info(f"[1] Attempting to get file: {file_id}")
            
            # Log available files for debugging
            logger.info(f"Available files: {list(StorageService._files.keys())}")
            
            if file_id not in StorageService._files:
                logger.error(f"[2] File not found: {file_id}")
                raise FileNotFoundError(f"File not found: {file_id}")
                
            return StorageService._files[file_id]
            
        except Exception as e:
            logger.error(f"Error retrieving file: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    async def cleanup_file(self, file_id: str) -> None:
        """Remove file from storage"""
        try:
            if file_id in StorageService._files:
                del StorageService._files[file_id]
                logger.info(f"File cleaned up: {file_id}")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
            raise

    async def cleanup_all(self) -> None:
        """Clear all files from storage"""
        try:
            StorageService._files.clear()
            logger.info("Cleared all files from memory")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
            raise