import uvicorn
import config
from project_settings import settings

if __name__ == "__main__":
    uvicorn.run(
        "config:app",
        host="127.0.0.1",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )

    print(f"Starting{config.PROJECT_NAME} v{config.VERSION}"
          f"in {'DEBUG' if config.DEBUG_MODE else 'PRODUCTION'} mode ...")
