
import time

def retry_api_call(max_attempts=3, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempt = 1
            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} failed: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    attempt += 1
                    time.sleep(delay)
            print(f"Failed to execute {func.__name__} after {max_attempts} attempts. Exiting.")
            exit(1)
        return wrapper
    return decorator
