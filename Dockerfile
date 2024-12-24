FROM debian:bullseye

ENV DEBIAN_FRONTEND=noninteractive

# Install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    liburcu-dev \
    sysstat \
    lm-sensors \
    smartmontools \
    zenity \
    pandoc \
    curl \
    net-tools \
    iproute2 \
    x11-utils \
    xauth \
    lshw \
    xdg-utils \
    mesa-utils \
    bc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create log directory with permissions
RUN mkdir -p /var/log/system_monitor && chmod -R 777 /var/log/system_monitor

# Copy the main script into the container
COPY system_monitor_gui.sh /usr/local/bin/system_monitor_gui.sh

# Make the script executable
RUN chmod +x /usr/local/bin/system_monitor_gui.sh

# Set default command
CMD ["/usr/local/bin/system_monitor_gui.sh"]
