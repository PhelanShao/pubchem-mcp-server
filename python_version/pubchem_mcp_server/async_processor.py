"""
Asynchronous Processing Module

Provides functionality for asynchronous processing of PubChem API requests.
"""

import asyncio
import logging
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, Optional, Callable, Union

from .pubchem_api import get_pubchem_data

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Status constants
STATUS_PENDING = 'pending'
STATUS_PROCESSING = 'processing'
STATUS_COMPLETED = 'completed'
STATUS_FAILED = 'failed'


class RequestStatus:
    """Status information for a request"""
    
    def __init__(self, request_id: str, query: str, format: str, include_3d: bool):
        self.request_id = request_id
        self.query = query
        self.format = format
        self.include_3d = include_3d
        self.status = STATUS_PENDING
        self.result = None
        self.error = None
        self.created_at = time.time()
        self.updated_at = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert status to dictionary"""
        return {
            'request_id': self.request_id,
            'query': self.query,
            'format': self.format,
            'include_3d': self.include_3d,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'result': self.result if self.status == STATUS_COMPLETED else None,
            'error': self.error if self.status == STATUS_FAILED else None
        }


class AsyncRequestProcessor:
    """Asynchronous request processor for PubChem API requests"""
    
    def __init__(self, max_workers: int = 4, status_ttl: int = 3600):
        """
        Initialize asynchronous request processor
        
        Args:
            max_workers: Maximum number of worker threads (default: 4)
            status_ttl: Time to live for completed request statuses in seconds (default: 1 hour)
        """
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.status_map: Dict[str, RequestStatus] = {}
        self.status_lock = threading.Lock()
        self.status_ttl = status_ttl
        self.cleanup_task = None
        
        # Start cleanup task
        self._start_cleanup_task()
    
    def _start_cleanup_task(self):
        """Start cleanup task to remove old completed requests"""
        async def cleanup_loop():
            while True:
                self._cleanup_old_statuses()
                await asyncio.sleep(300)  # Run every 5 minutes
        
        loop = asyncio.new_event_loop()
        self.cleanup_task = loop.create_task(cleanup_loop())
        
        def run_cleanup():
            asyncio.set_event_loop(loop)
            loop.run_forever()
        
        cleanup_thread = threading.Thread(target=run_cleanup, daemon=True)
        cleanup_thread.start()
    
    def _cleanup_old_statuses(self):
        """Clean up old completed request statuses"""
        now = time.time()
        with self.status_lock:
            to_remove = []
            for request_id, status in self.status_map.items():
                if status.status in (STATUS_COMPLETED, STATUS_FAILED) and now - status.updated_at > self.status_ttl:
                    to_remove.append(request_id)
            
            for request_id in to_remove:
                logger.info(f"Cleaning up old status for request {request_id}")
                del self.status_map[request_id]
    
    def submit_request(self, query: str, format: str = 'JSON', include_3d: bool = False) -> str:
        """
        Submit a new request for processing
        
        Args:
            query: Compound name or PubChem CID
            format: Output format, options: "JSON", "CSV", or "XYZ", default: "JSON"
            include_3d: Whether to include 3D structure information (only valid when format is "XYZ"), default: False
            
        Returns:
            Request ID
        """
        # Generate request ID
        request_id = str(uuid.uuid4())
        
        # Create request status
        status = RequestStatus(request_id, query, format, include_3d)
        
        # Add to status map
        with self.status_lock:
            self.status_map[request_id] = status
        
        # Submit to executor
        self.executor.submit(self._process_request, request_id)
        
        logger.info(f"Submitted new request {request_id} for query: {query}")
        return request_id
    
    def _process_request(self, request_id: str):
        """Process a request in background thread"""
        with self.status_lock:
            if request_id not in self.status_map:
                logger.warning(f"Request {request_id} not found in status map")
                return
            
            status = self.status_map[request_id]
            status.status = STATUS_PROCESSING
            status.updated_at = time.time()
        
        logger.info(f"Processing request {request_id} for query: {status.query}")
        
        try:
            # Get PubChem data
            result = get_pubchem_data(status.query, status.format, status.include_3d)
            
            # Update status
            with self.status_lock:
                if request_id in self.status_map:
                    status = self.status_map[request_id]
                    status.status = STATUS_COMPLETED
                    status.result = result
                    status.updated_at = time.time()
                    logger.info(f"Request {request_id} completed successfully")
                else:
                    logger.warning(f"Request {request_id} not found in status map after processing")
        except Exception as e:
            logger.error(f"Error processing request {request_id}: {e}")
            
            # Update status
            with self.status_lock:
                if request_id in self.status_map:
                    status = self.status_map[request_id]
                    status.status = STATUS_FAILED
                    status.error = str(e)
                    status.updated_at = time.time()
                else:
                    logger.warning(f"Request {request_id} not found in status map after error")
    
    def get_status(self, request_id: str) -> Optional[Dict[str, Any]]:
        """
        Get status for a request
        
        Args:
            request_id: Request ID
            
        Returns:
            Status dictionary or None if request ID not found
        """
        with self.status_lock:
            status = self.status_map.get(request_id)
            return status.to_dict() if status else None
    
    def shutdown(self):
        """Shutdown executor and cancel cleanup task"""
        self.executor.shutdown(wait=False)
        if self.cleanup_task:
            self.cleanup_task.cancel()


# Singleton instance
_processor_instance: Optional[AsyncRequestProcessor] = None


def get_processor() -> AsyncRequestProcessor:
    """Get the singleton processor instance"""
    global _processor_instance
    if _processor_instance is None:
        _processor_instance = AsyncRequestProcessor()
    return _processor_instance
