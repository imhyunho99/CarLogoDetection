import time
import logging
from django.utils.deprecation import MiddlewareMixin

class PerformanceMonitoringMiddleware(MiddlewareMixin):
    """Middleware to monitor request performance"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('performance')
        super().__init__(get_response)
    
    def process_request(self, request):
        request.start_time = time.time()
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            # Log performance metrics
            self.logger.info(
                f"method={request.method} "
                f"path={request.path} "
                f"status={response.status_code} "
                f"duration={duration:.3f}s "
                f"user_agent={request.META.get('HTTP_USER_AGENT', 'Unknown')[:50]}"
            )
            
            # Add performance header
            response['X-Response-Time'] = f"{duration:.3f}s"
        
        return response
