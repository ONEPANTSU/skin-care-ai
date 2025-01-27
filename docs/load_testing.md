# Load Testing

### Test Command
```bash
siege -c 10 -r 100 http://0.0.0.0:8888/
```

### Results
| Metric                           | Value              |
|----------------------------------|--------------------|
| Transactions                     | 3000 hits          |
| Availability                     | 100.00 %           |
| Elapsed time                     | 68.26 secs         |
| Data transferred                 | 121.85 MB          |
| Response time                    | 205.03 ms          |
| Transaction rate                 | 43.95 trans/sec    |
| Throughput                       | 1.79 MB/sec        |
| Concurrency                      | 9.01               |
| Successful transactions           | 3000               |
| Failed transactions              | 0                  |
| Longest transaction              | 4040.00 ms         |
| Shortest transaction             | 0.00 ms            |
