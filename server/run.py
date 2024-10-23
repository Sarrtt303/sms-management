from app import create_app
import logging

app = create_app()

if __name__ == '__main__':
    # Set up logging for better visibility
    logging.basicConfig(level=logging.INFO)
    
    # Log that the app is starting
    logging.info("Starting the Flask application...")

    try:
        # Run the app and display a success message if MongoDB connection is successful
        app.run()
    except Exception as e:
        logging.error(f"An error occurred while running the app: {e}")
