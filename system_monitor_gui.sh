#!/bin/bash

# GUI for Enhanced System Monitoring using Zenity

LOG_DIR="/var/log/system_monitor"
REPORT_FILE="reports/system_report.html"

# Function to generate a report using the Python script
generate_report() {
    if command -v python3 &>/dev/null; then
        python3 generate_report.py
        if [ $? -eq 0 ]; then
            zenity --info --title="🎉 Report Ready!" --text="Your system report has been successfully generated and saved as:\n\n<b>$REPORT_FILE</b>\n\nClick 'View Report' to open it."
        else
            zenity --error --title="Oops! 😟" --text="Report generation failed. Please check the Python script or logs."
        fi
    else
        zenity --error --title="Python Missing" --text="Python3 is not installed or not in the PATH.\n\nPlease install Python3 to proceed."
    fi
}

# Function to view the HTML report in the default browser
view_report() {
    if [ -f "$REPORT_FILE" ]; then
        xdg-open "$REPORT_FILE" &>/dev/null || zenity --error --title="Browser Issue" --text="Failed to open the report.\nEnsure you have a web browser installed."
    else
        zenity --error --title="Report Not Found" --text="No report found! Please generate one before viewing."
    fi
}

# Function to configure alerts
configure_alerts() {
    thresholds=$(zenity --forms --title="🔔 Configure Alerts" \
        --text="Set the alert thresholds:" \
        --add-entry="Max CPU Temperature (°C)" \
        --add-entry="Max CPU Usage (%)" \
        --add-entry="Max Memory Usage (%)")

    if [ $? -eq 0 ]; then
        cpu_temp_threshold=$(echo "$thresholds" | cut -d'|' -f1)
        cpu_usage_threshold=$(echo "$thresholds" | cut -d'|' -f2)
        memory_usage_threshold=$(echo "$thresholds" | cut -d'|' -f3)

        echo "CPU_TEMP_THRESHOLD=$cpu_temp_threshold" > alert_config.txt
        echo "CPU_USAGE_THRESHOLD=$cpu_usage_threshold" >> alert_config.txt
        echo "MEMORY_USAGE_THRESHOLD=$memory_usage_threshold" >> alert_config.txt

        zenity --info --title="Alerts Updated" --text="Your alert thresholds have been saved successfully! 🎯"
    else
        zenity --warning --title="Configuration Cancelled" --text="No changes were made to alert thresholds."
    fi
}

# Function to monitor logs in real-time
view_logs() {
    if [ -f "$LOG_DIR/system_monitor.log" ]; then
        zenity --text-info --title="📜 Real-Time System Logs" --width=800 --height=500 --filename="$LOG_DIR/system_monitor.log" --editable
    else
        zenity --error --title="Log Not Found" --text="No logs available. Please ensure the monitoring service is running."
    fi
}

# Function to display help and guidance
show_help() {
    zenity --info --title="💡 Help - System Monitor" \
        --text="Welcome to the System Monitor GUI!\n\nHere are the available features:\n
1. <b>Generate Report:</b> Creates a detailed system report.
2. <b>View Report:</b> Opens the most recent system report.
3. <b>Configure Alerts:</b> Set CPU, memory, and temperature thresholds for alerts.
4. <b>View Logs:</b> View system logs for troubleshooting.\n\nFor any issues, contact support or refer to the logs."
}

# Main GUI menu
while true; do
    action=$(zenity --list --title="🚀 System Monitor Dashboard" \
        --text="Choose an action:" \
        --column="Action" --column="Description" --width=500 --height=350 \
        "Generate Report" "Create a new system report" \
        "View Report" "Open the most recent system report" \
        "Configure Alerts" "Set thresholds for alerts" \
        "View Logs" "View live system logs" \
        "Help" "Learn how to use this tool" \
        "Exit" "Close the application")

    case "$action" in
        "Generate Report")
            generate_report
            ;;
        "View Report")
            view_report
            ;;
        "Configure Alerts")
            configure_alerts
            ;;
        "View Logs")
            view_logs
            ;;
        "Help")
            show_help
            ;;
        "Exit")
            break
            ;;
        *)
            zenity --error --title="Invalid Selection" --text="Please select a valid option from the menu."
            break
	    ;;
    esac
done
