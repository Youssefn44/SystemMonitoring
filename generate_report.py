import os
import json
from datetime import datetime

# Define log directory and report output
LOG_DIR = "/var/log/system_monitor"
REPORT_FILE = "reports/system_report.html"

# HTML Template with updated styles (Black and Blue colors, charts side by side)
HTML_TEMPLATE = """
<html>
<head>
    <title>System Monitoring Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #121212;
            color: #ffffff;
        }}
        h1, h2 {{
            color: #2980b9;
            text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.3);
        }}
        hr {{
            border: 1px solid #2980b9;
        }}
        canvas {{
            margin: 20px 10px;
            border: 2px solid #2980b9;
            border-radius: 8px;
            background-color: #1a1a1a;
        }}
        .container {{
            margin: 0 auto;
            max-width: 1200px;
        }}
        .chart-container {{
            display: flex;
            justify-content: space-between;
            gap: 20px;
            flex-wrap: wrap;
        }}
        .chart-container canvas {{
            width: 45%;
            height: 300px;
        }}
        pre {{
            background-color: #2c3e50;
            padding: 15px;
            border-radius: 5px;
            color: #ecf0f1;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>System Monitoring Report</h1>
        <p>Generated on: {date}</p>
        <hr>
        <h2>CPU Temperature</h2>
        <pre>{cpu_temp}</pre>
        <h2>System Usage</h2>
        <div class="chart-container">
            <canvas id="cpuUsageChart"></canvas>
            <canvas id="memoryUsageChart"></canvas>
        </div>
        <h2>Disk Usage</h2>
        <pre>{disk_usage}</pre>
        <h2>System Load</h2>
        <pre>{system_load}</pre>
        <h2>SMART Status</h2>
        <pre>{smart_status}</pre>
        <h2>Network Statistics</h2>
        <pre>{network_stats}</pre>
    </div>

    <script>
        // CPU Usage Data
        const cpuUsageLabels = {cpu_usage_labels};
        const cpuUsageData = {cpu_usage_data};
        const cpuUsageCtx = document.getElementById('cpuUsageChart').getContext('2d');
        new Chart(cpuUsageCtx, {{
            type: 'line',
            data: {{
                labels: cpuUsageLabels,
                datasets: [{{
                    label: 'CPU Usage (%)',
                    data: cpuUsageData,
                    borderColor: 'rgba(41, 128, 185, 1)',
                    backgroundColor: 'rgba(41, 128, 185, 0.2)',
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});

        // Memory Usage Data
        const memoryUsageLabels = {memory_usage_labels};
        const memoryUsageData = {memory_usage_data};
        const memoryUsageCtx = document.getElementById('memoryUsageChart').getContext('2d');
        new Chart(memoryUsageCtx, {{
            type: 'bar',
            data: {{
                labels: memoryUsageLabels,
                datasets: [{{
                    label: 'Memory Usage (GiB)',
                    data: memoryUsageData,
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

def read_log(file_path):
    """Read log data from a file."""
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return file.read().strip()
    return "No data available"

def parse_cpu_usage(raw_cpu_usage):
    """Parse CPU usage log and return labels and data."""
    try:
        # Clean up the raw log data and split by lines
        lines = raw_cpu_usage.strip().splitlines()
        
        # Ensure there's only one line and it's in the correct format
        if len(lines) == 1 and "CPU Usage:" in lines[0]:
            cpu_usage = float(lines[0].split(":")[-1].strip().replace("%", ""))
            return ["CPU Usage"], [cpu_usage]
        
        # If the format doesn't match, return an error
        return ["Error"], [0]
    except Exception as e:
        print(f"Error parsing CPU usage: {e}")
        return ["Error"], [0]

def parse_memory_usage(raw_memory_usage):
    """Parse memory usage log and return labels and data."""
    try:
        # Assuming the log has a single line with 'Memory Usage: 18.60%'
        lines = raw_memory_usage.splitlines()
        labels = ["Memory Usage"]
        data = [float(lines[0].split(":")[-1].strip().replace("%", ""))]
        return labels, data
    except Exception as e:
        return ["Error"], [0]

def generate_report():
    """Generate the interactive HTML report."""
    cpu_temp = read_log(os.path.join(LOG_DIR, "cpu_temp.log"))
    raw_cpu_usage = read_log(os.path.join(LOG_DIR, "cpu_usage.log"))
    cpu_usage_labels, cpu_usage_data = parse_cpu_usage(raw_cpu_usage)
    disk_usage = read_log(os.path.join(LOG_DIR, "disk_usage.log"))
    raw_memory_usage = read_log(os.path.join(LOG_DIR, "memory_usage.log"))
    memory_usage_labels, memory_usage_data = parse_memory_usage(raw_memory_usage)
    system_load = read_log(os.path.join(LOG_DIR, "system_load.log"))
    smart_status = read_log(os.path.join(LOG_DIR, "smart_status.log"))
    network_stats = read_log(os.path.join(LOG_DIR, "network_stats.log"))

    # Generate HTML content
    html_content = HTML_TEMPLATE.format(
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        cpu_temp=cpu_temp or "Data unavailable",
        cpu_usage_labels=json.dumps(cpu_usage_labels),
        cpu_usage_data=json.dumps(cpu_usage_data),
        disk_usage=disk_usage or "No data available",
        memory_usage_labels=json.dumps(memory_usage_labels),
        memory_usage_data=json.dumps(memory_usage_data),
        system_load=system_load or "No data available",
        smart_status=smart_status or "No data available",
        network_stats=network_stats or "No data available"
    )

    # Write the report to a file
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    with open(REPORT_FILE, "w") as report_file:
        report_file.write(html_content)

    print(f"Report generated: {REPORT_FILE}")

if __name__ == "__main__":
    generate_report()
