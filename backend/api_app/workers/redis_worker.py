"""Background worker tasks using Redis as a message broker."""

from typing import Any, Dict
import json
from loguru import logger
from datetime import datetime


class RedisWorker:
    """Redis-based background worker for async task processing."""

    def __init__(self, redis_client):
        self.redis = redis_client
        self.task_queue = "task_queue"
        self.result_prefix = "task_result:"

    async def enqueue_task(self, task_name: str, task_data: Dict[str, Any]) -> str:
        """
        Enqueue a task to be processed by worker.

        Args:
            task_name: Name of the task to execute
            task_data: Data/parameters for the task

        Returns:
            task_id: Unique identifier for the task
        """
        task_id = f"{task_name}:{datetime.utcnow().timestamp()}"
        task_payload = {
            "task_id": task_id,
            "task_name": task_name,
            "task_data": task_data,
            "created_at": datetime.utcnow().isoformat(),
            "status": "pending",
        }

        # Push task to Redis list (queue)
        await self.redis.lpush(self.task_queue, json.dumps(task_payload))
        logger.info(f"Task enqueued: {task_id}")

        return task_id

    async def get_task_result(self, task_id: str) -> Dict[str, Any] | None:
        """
        Get result of a completed task.

        Args:
            task_id: Task identifier

        Returns:
            Task result or None if not found
        """
        result_key = f"{self.result_prefix}{task_id}"
        result_data = await self.redis.get(result_key)

        if result_data:
            return json.loads(result_data)
        return None

    async def set_task_result(
        self, task_id: str, result: Any, status: str = "completed", expire: int = 3600
    ):
        """
        Store task result in Redis.

        Args:
            task_id: Task identifier
            result: Task result data
            status: Task status (completed, failed)
            expire: Time to live in seconds (default 1 hour)
        """
        result_key = f"{self.result_prefix}{task_id}"
        result_payload = {
            "task_id": task_id,
            "status": status,
            "result": result,
            "completed_at": datetime.utcnow().isoformat(),
        }

        await self.redis.setex(result_key, expire, json.dumps(result_payload))
        logger.info(f"Task result stored: {task_id} - Status: {status}")

    async def process_tasks(self):
        """
        Worker loop to process tasks from queue.
        This should run in a separate process/container.
        """
        logger.info("Worker started, waiting for tasks...")

        while True:
            try:
                # Block and wait for task (BRPOP with timeout)
                task_data = await self.redis.brpop(self.task_queue, timeout=5)

                if task_data:
                    _, task_json = task_data
                    task = json.loads(task_json)

                    logger.info(f"Processing task: {task['task_id']}")

                    try:
                        # Execute task based on task_name
                        result = await self._execute_task(
                            task["task_name"], task["task_data"]
                        )

                        # Store result
                        await self.set_task_result(
                            task["task_id"], result, status="completed"
                        )
                    except Exception as e:
                        logger.error(f"Task failed: {task['task_id']} - {str(e)}")
                        await self.set_task_result(
                            task["task_id"], {"error": str(e)}, status="failed"
                        )

            except Exception as e:
                logger.error(f"Worker error: {str(e)}")
                continue

    async def _execute_task(self, task_name: str, task_data: Dict[str, Any]) -> Any:
        """
        Execute task based on task name.

        Add your task handlers here.
        """
        if task_name == "send_email":
            return await self._send_email_task(task_data)
        elif task_name == "process_ticket":
            return await self._process_ticket_task(task_data)
        elif task_name == "generate_report":
            return await self._generate_report_task(task_data)
        else:
            raise ValueError(f"Unknown task: {task_name}")

    async def _send_email_task(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Example: Send email task."""
        # Implement email sending logic here
        logger.info(f"Sending email to: {data.get('to')}")
        return {"status": "email_sent", "to": data.get("to")}

    async def _process_ticket_task(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Example: Process ticket task."""
        # Implement ticket processing logic here
        logger.info(f"Processing ticket: {data.get('ticket_id')}")
        return {"status": "ticket_processed", "ticket_id": data.get("ticket_id")}

    async def _generate_report_task(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Example: Generate report task."""
        # Implement report generation logic here
        logger.info(f"Generating report: {data.get('report_type')}")
        return {"status": "report_generated", "report_type": data.get("report_type")}


# Task helper functions for easy task enqueueing
async def enqueue_email_task(redis_client, to: str, subject: str, body: str) -> str:
    """Enqueue an email sending task."""
    worker = RedisWorker(redis_client)
    return await worker.enqueue_task(
        "send_email", {"to": to, "subject": subject, "body": body}
    )


async def enqueue_ticket_processing(redis_client, ticket_id: str, user_id: str) -> str:
    """Enqueue a ticket processing task."""
    worker = RedisWorker(redis_client)
    return await worker.enqueue_task(
        "process_ticket", {"ticket_id": ticket_id, "user_id": user_id}
    )


async def enqueue_report_generation(
    redis_client, report_type: str, filters: Dict[str, Any]
) -> str:
    """Enqueue a report generation task."""
    worker = RedisWorker(redis_client)
    return await worker.enqueue_task(
        "generate_report", {"report_type": report_type, "filters": filters}
    )
