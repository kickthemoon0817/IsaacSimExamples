# === ISAAC SIM 5.0.0 ===
FROM nvcr.io/nvidia/isaac-sim:5.0.0 AS isaac-sim-5.0.0

# Environemt variables
ENV ISAAC_SIM_VERSION=5.0.0 ACCEPT_EULA=Y

WORKDIR /isaac-sim

# Create symlink for python -> python3
RUN ln -sf /isaac-sim/kit/python/bin/python3 /isaac-sim/kit/python/bin/python

# Setup bashrc to source Isaac Sim Python environment
RUN echo 'source /isaac-sim/setup_python_env.sh' >> ~/.bashrc

# Reset the entrypoint to bash
ENTRYPOINT ["/bin/bash"]


# === ISAAC SIM 4.5.0 ===
FROM nvcr.io/nvidia/isaac-sim:4.5.0 AS isaac-sim-4.5.0

# Environemt variables
ENV ISAAC_SIM_VERSION=4.5.0

WORKDIR /isaac-sim

# Create symlink for python -> python3
RUN ln -sf /isaac-sim/kit/python/bin/python3 /isaac-sim/kit/python/bin/python

# Setup bashrc to source Isaac Sim Python environment
RUN echo 'source /isaac-sim/setup_python_env.sh' >> /root/.bashrc

# Reset the entrypoint to bash
ENTRYPOINT ["/bin/bash"]


# === ISAAC SIM 4.2.0 ===
FROM nvcr.io/nvidia/isaac-sim:4.2.0 AS isaac-sim-4.2.0

# Environemt variables
ENV ISAAC_SIM_VERSION=4.2.0

WORKDIR /isaac-sim

# Create symlink for python -> python3
RUN ln -sf /isaac-sim/kit/python/bin/python3 /isaac-sim/kit/python/bin/python

# Setup bashrc to source Isaac Sim Python environment
RUN echo 'source /isaac-sim/setup_python_env.sh' >> /root/.bashrc

# Reset the entrypoint to bash
ENTRYPOINT ["/bin/bash"]
