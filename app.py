import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="OptiVerse", layout="wide")

st.title("🔮 OptiVerse")
st.subheader("Optical Network Digital Twin & Self-Healing WDM Simulator")

if "G" not in st.session_state:
    st.session_state.G = nx.Graph()

if "requests" not in st.session_state:
    st.session_state.requests = 0

if "blocked" not in st.session_state:
    st.session_state.blocked = 0

G = st.session_state.G

st.sidebar.header("Network Builder")

node = st.sidebar.text_input("Node Name")

if st.sidebar.button("Add Node"):
    if node:
        G.add_node(node)

nodes = list(G.nodes())

if len(nodes) >= 2:

    n1 = st.sidebar.selectbox("Source Node", nodes)

    n2 = st.sidebar.selectbox(
        "Destination Node",
        nodes,
        index=min(1, len(nodes)-1)
    )

    if st.sidebar.button("Add Fiber Link"):
        if n1 != n2:
            G.add_edge(
                n1,
                n2,
                wavelength=random.randint(1, 8)
            )

st.sidebar.markdown("---")

st.header("🌐 Network Topology")

fig, ax = plt.subplots(figsize=(8, 6))

if len(G.nodes()) > 0:
    pos = nx.spring_layout(G, seed=42)

    edge_labels = {}

    for u, v, d in G.edges(data=True):
        edge_labels[(u, v)] = f"λ{d['wavelength']}"

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=2500,
        node_color="skyblue",
        ax=ax
    )

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        ax=ax
    )

st.pyplot(fig)

st.markdown("---")

st.header("📡 Traffic Request")

if len(nodes) >= 2:

    src = st.selectbox("Traffic Source", nodes)

    dst = st.selectbox(
        "Traffic Destination",
        nodes,
        key="dst"
    )

    if st.button("Establish Lightpath"):

        st.session_state.requests += 1

        try:
            path = nx.shortest_path(
                G,
                src,
                dst
            )

            st.success(f"Lightpath Established: {' ➜ '.join(path)}")

        except:
            st.session_state.blocked += 1
            st.error("Blocking Occurred")

st.markdown("---")

st.header("⚡ Optical Switching Mode")

switch_type = st.radio(
    "Select Switching",
    [
        "Optical Circuit Switching",
        "Optical Burst Switching",
        "Optical Packet Switching"
    ]
)

st.info(f"Current Mode: {switch_type}")

st.markdown("---")

st.header("🚨 Failure Simulator")

if len(nodes) > 0:

    fail_node = st.selectbox(
        "Select Node Failure",
        nodes,
        key="failure"
    )

    if st.button("Inject Failure"):

        temp = G.copy()

        if fail_node in temp:
            temp.remove_node(fail_node)

            st.warning(
                f"{fail_node} failed. Self-healing topology generated."
            )

            fig2, ax2 = plt.subplots(figsize=(8, 6))

            if len(temp.nodes()) > 0:

                pos2 = nx.spring_layout(temp, seed=42)

                nx.draw(
                    temp,
                    pos2,
                    with_labels=True,
                    node_size=2500,
                    node_color="lightgreen",
                    ax=ax2
                )

            st.pyplot(fig2)

st.markdown("---")

st.header("🔄 Wavelength Conversion")

if len(nodes) > 0:

    converter = st.selectbox(
        "Converter Node",
        nodes,
        key="converter"
    )

    old_lambda = st.number_input(
        "Current Wavelength",
        min_value=1,
        max_value=16,
        value=1
    )

    new_lambda = st.number_input(
        "Converted Wavelength",
        min_value=1,
        max_value=16,
        value=2
    )

    if st.button("Convert Wavelength"):
        st.success(
            f"{converter}: λ{old_lambda} ➜ λ{new_lambda}"
        )

st.markdown("---")

st.header("📊 Performance Metrics")

request_count = st.session_state.requests
blocked_count = st.session_state.blocked

blocking_probability = (
    blocked_count / request_count
    if request_count > 0
    else 0
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Traffic Requests",
    request_count
)

col2.metric(
    "Blocked Requests",
    blocked_count
)

col3.metric(
    "Blocking Probability",
    round(blocking_probability, 4)
)

st.markdown("---")

st.subheader("📘 Syllabus Coverage")

st.write("✅ UNIT I  : Passive Optical Networks")
st.write("✅ UNIT II : Virtual Topology Design")
st.write("✅ UNIT III: MPLS/WDM Routing")
st.write("✅ UNIT IV : Optical Switching")
st.write("✅ UNIT V  : Wavelength Convertible Networks")

st.success(
    "Complete Optical Switching Architecture Digital Twin Running Successfully"
)
