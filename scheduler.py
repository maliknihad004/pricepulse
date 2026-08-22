from apscheduler.schedulers.blocking import BlockingScheduler

# Import the existing monitoring function
from monitor import monitor_products


# Create the scheduler
scheduler = BlockingScheduler()


# Run the product monitor every 30 minutes
@scheduler.scheduled_job("interval", minutes=30)
def scheduled_monitor():
    # Run the existing product monitoring process
    print("\nRunning scheduled price check...")
    monitor_products()


# Run the scheduler when this file is executed directly
if __name__ == "__main__":
    print("PricePulse scheduler started.")
    print("Products will be checked every 30 minutes.")

    # Run one check immediately when the scheduler starts
    monitor_products()

    # Keep the scheduler running
    scheduler.start()