# Event Search API Documentation

## Overview
The Event Search API allows you to search and filter events based on various criteria with pagination support.

## Endpoint

```
POST /api/v1/events/search
```

## Request Body

```json
{
  "name": "string (optional)",
  "event_type": "string (optional)",
  "start_date_from": "string (optional, YYYY-MM-DD format)",
  "start_date_to": "string (optional, YYYY-MM-DD format)"
}
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | No | Search events by name (partial match, case-insensitive) |
| `event_type` | string | No | Filter by exact event type |
| `start_date_from` | string | No | Filter events starting from this date (inclusive, format: YYYY-MM-DD, e.g., "2025-01-01") |
| `start_date_to` | string | No | Filter events starting until this date (inclusive, format: YYYY-MM-DD, e.g., "2025-12-31") |

### Query Parameters (Pagination)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number |
| `size` | integer | 50 | Number of items per page |

## Examples

### 1. Search by Name

Search for events with "concert" in the name:

```bash
curl -X POST "http://localhost:8000/api/v1/events/search" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "concert"
  }'
```

### 2. Filter by Event Type

Get all "music" events:

```bash
curl -X POST "http://localhost:8000/api/v1/events/search" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "music"
  }'
```

### 3. Filter by Date Range

Get events starting between specific dates:

```bash
curl -X POST "http://localhost:8000/api/v1/events/search" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date_from": "2025-01-01",
    "start_date_to": "2025-12-31"
  }'
```

### 4. Combined Search with Pagination

Search for music concerts in 2025, page 2 with 10 results:

```bash
curl -X POST "http://localhost:8000/api/v1/events/search?page=2&size=10" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "concert",
    "event_type": "music",
    "start_date_from": "2025-01-01",
    "start_date_to": "2025-12-31"
  }'
```

### 5. Empty Search (Get All Events)

```bash
curl -X POST "http://localhost:8000/api/v1/events/search" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 6. Search by Specific Date

Get all events starting on a specific date:

```bash
curl -X POST "http://localhost:8000/api/v1/events/search" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date_from": "2025-06-15",
    "start_date_to": "2025-06-15"
  }'
```

### 7. Search Events Starting After a Date

Get all events starting from January 1, 2025 onwards:

```bash
curl -X POST "http://localhost:8000/api/v1/events/search" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date_from": "2025-01-01"
  }'
```

### 8. Search Events Before a Date

Get all events starting before December 31, 2025:

```bash
curl -X POST "http://localhost:8000/api/v1/events/search" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date_to": "2025-12-31"
  }'
```

## Response Format

```json
{
  "items": [
    {
      "id": "507f1f77bcf86cd799439011",
      "name": "Music Concert",
      "image_id": null,
      "description": "Amazing music event",
      "event_type": "music",
      "start_date": "2024-06-15T19:00:00",
      "end_date": "2024-06-15T23:00:00",
      "booking_start_date": "2024-05-01T00:00:00",
      "booking_end_date": "2024-06-14T23:59:59",
      "ticket_types": [
        {
          "name": "VIP",
          "total": 100,
          "price": 1500,
          "remaining": 50,
          "ticket_id": "abc123..."
        }
      ]
    }
  ],
  "total": 1,
  "page": 1,
  "size": 50,
  "pages": 1
}
```

## Response Fields

| Field | Description |
|-------|-------------|
| `items` | Array of event objects matching the search criteria |
| `total` | Total number of events matching the criteria |
| `page` | Current page number |
| `size` | Number of items per page |
| `pages` | Total number of pages |

## Features

1. **Case-Insensitive Search**: Name search is case-insensitive
2. **Partial Match**: Name search matches partial strings (e.g., "concert" matches "Rock Concert")
3. **Multiple Filters**: Combine multiple search criteria
4. **Date Range**: Filter events by start date range
5. **Pagination**: Control page size and navigate through results

## Notes

- All search parameters are optional
- Empty search body returns all events (with pagination)
- **Date Format**: Use `YYYY-MM-DD` format for dates (e.g., "2025-01-01")
- Date filters apply to the event's `start_date` field
- `start_date_from` includes the entire day from 00:00:00
- `start_date_to` includes the entire day until 23:59:59.999999
- Both date boundaries are inclusive
- The search uses MongoDB's regex for name matching
- Results are paginated by default (50 items per page)
