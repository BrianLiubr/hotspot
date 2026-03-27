from app.services.refresh.pipeline import run_refresh


if __name__ == "__main__":
    print(run_refresh(trigger_type="manual"))
