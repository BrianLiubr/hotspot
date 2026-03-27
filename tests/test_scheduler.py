from app.scheduler import scheduler


def test_scheduler_job_registered_once():
    scheduler.remove_all_jobs()
    assert len(scheduler.get_jobs()) == 0
