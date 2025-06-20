import time
import logging
from functools import wraps

logger = logging.getLogger('limiter')

rate_limit_store = {}

def rate_limiter(max_requests: int, time_window: int):
    """
    Rate limiting decorator.

    Parameters:
        max_requests (int): Maximum allowed requests within the time window.
        time_window (int): Time window in seconds.

    Returns:
        function: A decorated function with rate limiting.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = kwargs.get('user_id')  # Identify user (modify as needed)
            current_time = time.time()
            
            if user_id not in rate_limit_store:
                rate_limit_store[user_id] = []
            
            request_times = rate_limit_store[user_id]
            request_times = [t for t in request_times if current_time - t < time_window]

            if len(request_times) >= max_requests:
                logger.warning(f"Rate limit exceeded for user {user_id}. Try again later.")
                return {"error": "Rate limit exceeded. Try again later."}

            request_times.append(current_time)
            rate_limit_store[user_id] = request_times

            return func(*args, **kwargs)
        
        return wrapper
    return decorator
