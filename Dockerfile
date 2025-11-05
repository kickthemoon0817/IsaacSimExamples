# === ISAAC SIM 5.1.0 ===
FROM nvcr.io/nvidia/isaac-sim:5.1.0 AS isaac-sim-5.1.0
ENV ISAAC_SIM_VERSION=5.1.0 \
    ACCEPT_EULA=Y \
    PATH="/isaac-sim/kit/python/bin:${PATH}"
WORKDIR /isaac-sim

RUN ln -sf /isaac-sim/kit/python/bin/python3 /isaac-sim/kit/python/bin/python

ENTRYPOINT ["/bin/bash"]


# === ISAAC SIM 5.0.0 ===
FROM nvcr.io/nvidia/isaac-sim:5.0.0 AS isaac-sim-5.0.0
ENV ISAAC_SIM_VERSION=5.0.0 \
    ACCEPT_EULA=Y \
    PATH="/isaac-sim/kit/python/bin:${PATH}"
WORKDIR /isaac-sim

RUN ln -sf /isaac-sim/kit/python/bin/python3 /isaac-sim/kit/python/bin/python

ENTRYPOINT ["/bin/bash"]


# === ISAAC SIM 4.5.0 ===
FROM nvcr.io/nvidia/isaac-sim:4.5.0 AS isaac-sim-4.5.0
ENV ISAAC_SIM_VERSION=4.5.0 \
    ACCEPT_EULA=Y \
    PATH="/isaac-sim/kit/python/bin:${PATH}"
WORKDIR /isaac-sim

RUN ln -sf /isaac-sim/kit/python/bin/python3 /isaac-sim/kit/python/bin/python

ENTRYPOINT ["/bin/bash"]


# === ISAAC SIM 4.2.0 ===
FROM nvcr.io/nvidia/isaac-sim:4.2.0 AS isaac-sim-4.2.0
ENV ISAAC_SIM_VERSION=4.2.0 \
    ACCEPT_EULA=Y \
    PATH="/isaac-sim/kit/python/bin:${PATH}"
WORKDIR /isaac-sim

RUN ln -sf /isaac-sim/kit/python/bin/python3 /isaac-sim/kit/python/bin/python

ENTRYPOINT ["/bin/bash"]
